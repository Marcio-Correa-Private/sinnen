import { chromium } from 'playwright';
import { readFileSync } from 'fs';

const DATA = JSON.parse(readFileSync('/home/claude/work/fixtures.json', 'utf8'));

const b64u = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
const jwt = `${b64u({alg:'HS256',typ:'JWT'})}.${b64u({sub:'u1',aud:'authenticated',role:'authenticated',email:'correa.marcio1@gmail.com',exp:9999999999})}.sig`;

// --- mini PostgREST filter engine -------------------------------------------
const cmp = (a, b) => (a === null || a === undefined) ? -1 : (b === null || b === undefined) ? 1 : (a > b ? 1 : a < b ? -1 : 0);

function applyFilters(rows, params) {
  let out = rows.slice();
  for (const [key, raw] of params.entries()) {
    if (['select','order','limit','offset'].includes(key)) continue;
    const i = raw.indexOf('.');
    const op = raw.slice(0, i), val = raw.slice(i + 1);
    out = out.filter(r => {
      const v = r[key];
      switch (op) {
        case 'eq':  return String(v) === val;
        case 'neq': return String(v) !== val;
        case 'gte': return cmp(v, val) >= 0;
        case 'lte': return cmp(v, val) <= 0;
        case 'gt':  return cmp(v, val) > 0;
        case 'lt':  return cmp(v, val) < 0;
        case 'is':  return val === 'null' ? (v === null || v === undefined) : String(v) === val;
        case 'ilike': {
          const re = new RegExp('^' + val.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/%/g, '.*') + '$', 'i');
          return v != null && re.test(String(v));
        }
        default: return true;
      }
    });
  }
  const ord = params.get('order');
  if (ord) {
    const specs = ord.split(',').map(s => { const [c, ...m] = s.split('.'); return { c, desc: m.includes('desc') }; });
    out.sort((a, b) => { for (const s of specs) { const d = cmp(a[s.c], b[s.c]); if (d) return s.desc ? -d : d; } return 0; });
  }
  const lim = params.get('limit');
  if (lim) out = out.slice(0, Number(lim));
  return out;
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

await page.route('**/auth/v1/**', route => {
  const u = route.request().url();
  const user = { id:'u1', aud:'authenticated', role:'authenticated', email:'correa.marcio1@gmail.com', app_metadata:{provider:'email'}, user_metadata:{}, created_at:'2026-07-27T10:00:00Z' };
  if (u.includes('/token')) {
    route.fulfill({ json: { access_token: jwt, token_type:'bearer', expires_in:3600, expires_at:9999999999, refresh_token:'r1', user } });
  } else if (u.includes('/user')) {
    route.fulfill({ json: user });
  } else if (u.includes('/logout')) {
    route.fulfill({ status: 204, body: '' });
  } else { route.fulfill({ json: {} }); }
});

await page.route('**/rest/v1/**', route => {
  const req = route.request();
  const u = new URL(req.url());
  const table = u.pathname.split('/rest/v1/')[1];
  const method = req.method();
  const headers = req.headers();
  const accept = headers['accept'] || '';
  const prefer = headers['prefer'] || '';

  if (method !== 'GET' && method !== 'HEAD') { // writes: acknowledge without mutating fixtures
    route.fulfill({ status: 200, headers: { 'content-type': 'application/json' }, body: JSON.stringify(prefer.includes('return=representation') ? [{ id: 'new-id' }] : []) });
    return;
  }

  const rows = applyFilters(DATA[table] ?? [], u.searchParams);
  const h = {
    'content-type': 'application/json',
    'content-range': `0-${Math.max(rows.length - 1, 0)}/${rows.length}`,
    'access-control-expose-headers': 'content-range',
  };
  if (method === 'HEAD' || prefer.includes('head=true')) { route.fulfill({ status: 200, headers: h, body: '' }); return; }
  if (accept.includes('vnd.pgrst.object')) { route.fulfill({ status: 200, headers: h, body: JSON.stringify(rows[0] ?? {}) }); return; }
  route.fulfill({ status: 200, headers: h, body: JSON.stringify(rows) });
});

const ROOT = new URL('..', import.meta.url).pathname;
const shot = async (name) => { await page.screenshot({ path: `${ROOT}test/shots/${name}.png`, fullPage: true }); };

await page.goto(`file://${ROOT}dist/index.html`);
await page.waitForTimeout(500);
await shot('01-login');
await page.fill('#authEmail', 'correa.marcio1@gmail.com');
await page.fill('#authPass', 'Oleos#2026');
await page.click('#btnLogin');
await page.waitForSelector('#app:not(.hidden)', { timeout: 10000 });
await page.waitForTimeout(1200);
await shot('02-painel');

for (const [tab, name] of [['venda','03-venda'],['pedidos','04-pedidos'],['clientes','05-clientes'],['produtos','06-produtos'],['mais','07-mais']]) {
  const sel = `#tabs button[data-tab="${tab}"]`;
  if (await page.$(sel)) { await page.click(sel); await page.waitForTimeout(900); await shot(name); }
}

// sub-sections under "mais"
for (const [id, name] of [['estoque','08-estoque'],['lotes','08b-lotes'],['despesas','09-despesas'],['socios','10-socios']]) {
  const btn = await page.$(`[data-mais="${id}"], [onclick*="desenhaMais('${id}')"]`);
  if (btn) { await btn.click(); await page.waitForTimeout(1000); await shot(name); }
}

console.log(JSON.stringify({ errors }, null, 1));
await browser.close();
