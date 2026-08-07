import base64, re, io

src = open('app-v2.html', encoding='utf-8').read()
orig_len = len(src)

def b64(p):
    return base64.b64encode(open(p,'rb').read()).decode()

# ---------- 1. fonts ----------
faces = []
for w in (400,500,600,700,800):
    faces.append(
        "@font-face{font-family:'Poppins';font-style:normal;font-weight:%d;font-display:swap;"
        "src:url(data:font/woff2;base64,%s) format('woff2');"
        "unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
        "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}"
        % (w, b64('fonts/Poppins-%d.woff2' % w)))
FONTS = "\n".join(faces)

# ---------- 2. head ----------
src = src.replace('<meta name="theme-color" content="#2f6f4f">',
                  '<meta name="theme-color" content="#1F2A24">')
src = src.replace('<title>Gestão · Óleos Essenciais</title>',
                  '<title>SINNEN · Gestão</title>')

icon_b64 = base64.b64encode(open('icon.svg','rb').read()).decode()
src = re.sub(r'<link rel="icon" href="data:image/svg\+xml;base64,[^"]*">',
             '<link rel="icon" href="data:image/svg+xml;base64,%s">' % icon_b64, src)
src = re.sub(r'<link rel="apple-touch-icon" href="data:image/svg\+xml;base64,[^"]*">',
             '<link rel="apple-touch-icon" href="data:image/svg+xml;base64,%s">' % icon_b64, src)

# ---------- 3. tokens ----------
OLD_ROOT = src[src.index(':root{'):src.index('*{box-sizing')]
NEW_ROOT = """:root{
  /* ===== SINNEN — cores da marca ===== */
  --pinho:#1F2A24; --salva:#8FAE8B; --linho:#F7F5EF; --lavanda:#B7A6D4;
  /* ===== superfícies ===== */
  --bg:#EDEBE4; --card:#F9F8F3; --line:#DFDCD2; --fill:#E7E4DA;
  /* ===== texto ===== */
  --ink:#1F2A24; --muted:#556059; --on-dark:#F7F5EF;
  /* ===== ações ===== */
  --brand:#1F2A24; --brand-dark:#121A15; --brand-soft:#E2EADF;
  --accent:#8FAE8B; --accent-soft:#E2EADF;
  /* ===== estados ===== */
  --ok:#356043; --ok-soft:#E2EADF;
  --warn:#7A5B12; --warn-soft:#F2EAD3;
  --danger:#8F3A2B; --danger-soft:#F6E4DF;
  --info:#5B4A80; --info-soft:#EFEAF7;
  /* ===== forma ===== */
  --radius:16px; --radius-sm:12px;
  --shadow:0 1px 2px rgba(31,42,36,.05), 0 6px 18px rgba(31,42,36,.055);
  --shadow-lg:0 14px 46px rgba(31,42,36,.20);
  --ring:0 0 0 3px rgba(143,174,139,.42);
  --tap:46px;
}
"""
src = src.replace(OLD_ROOT, FONTS + "\n" + NEW_ROOT)

# ---------- 4. tipografia ----------
src = src.replace(
 'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",sans-serif;background:var(--bg);color:var(--ink);font-size:16px;line-height:1.45}',
 'body{font-family:"Poppins",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--ink);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;letter-spacing:-.005em}')

# Poppins runs large/round: normalise the odd weights to the 5 embedded cuts
for a,b in (('font-weight:750','font-weight:700'),('font-weight:650','font-weight:600'),
            ('font-weight:850','font-weight:800')):
    src = src.replace(a,b)

# ---------- 5. componentes ----------
REPL = [
 # inputs
 ("input,select,textarea{font:inherit;width:100%;min-height:var(--tap);padding:11px 13px;border:1.5px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);appearance:none}",
  "input,select,textarea{font:inherit;width:100%;min-height:var(--tap);padding:11px 13px;border:1.5px solid var(--line);border-radius:var(--radius-sm);background:#fff;color:var(--ink);appearance:none;transition:border-color .15s,box-shadow .15s}"),
 ("stroke='%235d6b62'", "stroke='%23556059'"),
 ("input:focus,select:focus,textarea:focus{outline:none;border-color:var(--brand);box-shadow:0 0 0 3px rgba(47,111,79,.14)}",
  "input:focus,select:focus,textarea:focus{outline:none;border-color:var(--salva);box-shadow:var(--ring)}"),
 (":focus-visible{outline:2px solid var(--brand);outline-offset:2px}",
  ":focus-visible{outline:2px solid var(--salva);outline-offset:2px}"),
 # botões
 (".btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:50px;padding:13px 16px;border-radius:13px;background:var(--brand);color:#fff;font-weight:700;font-size:16px;text-align:center;margin-top:14px;transition:transform .06s, background .15s}",
  ".btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:50px;padding:13px 16px;border-radius:var(--radius-sm);background:var(--brand);color:var(--on-dark);font-weight:600;font-size:16px;letter-spacing:.01em;text-align:center;margin-top:14px;transition:transform .06s, background .15s}"),
 (".btn.secondary{background:var(--brand-soft);color:var(--brand-dark)}",
  ".btn.secondary{background:var(--brand-soft);color:var(--brand-dark)}\n.btn.secondary:active{background:#d5e0d1}"),
 (".btn.danger{background:#fdecec;color:#b3261e}", ".btn.danger{background:var(--danger-soft);color:var(--danger)}"),
 (".btn.danger:active{background:#f9d9d9}", ".btn.danger:active{background:#efd3cc}"),
 (".link{color:var(--brand);font-weight:600;text-align:center;display:block;margin-top:16px;font-size:14.5px;padding:10px;min-height:var(--tap)}",
  ".link{color:var(--brand);font-weight:600;text-align:center;display:block;margin-top:16px;font-size:14.5px;padding:10px;min-height:var(--tap);text-decoration:underline;text-decoration-color:var(--salva);text-underline-offset:4px;text-decoration-thickness:2px}"),
 # cartões
 (".card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px;margin-bottom:12px}",
  ".card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px;margin-bottom:12px}"),
 # login
 (".logo .mark{width:76px;height:76px;margin:0 auto 15px;filter:drop-shadow(0 8px 20px rgba(47,111,79,.30))}",
  ".logo .mark{width:72px;height:72px;margin:0 auto 18px;filter:drop-shadow(0 10px 22px rgba(31,42,36,.22))}"),
 (".logo h1{font-size:22px;font-weight:700;letter-spacing:-.01em}",
  ".logo .word{width:132px;margin:0 auto 8px;color:var(--pinho)}\n.logo .word svg{width:100%;height:auto;display:block}\n.logo h1{font-size:13px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}"),
 (".logo p{color:var(--muted);font-size:14.5px;margin-top:3px}",
  ".logo p{color:var(--muted);font-size:14.5px;margin-top:10px;letter-spacing:0}"),
 (".pw-toggle{position:absolute;right:6px;top:50%;transform:translateY(-50%);min-height:38px;padding:6px 12px;font-size:13.5px;font-weight:700;color:var(--brand);border-radius:9px}",
  ".pw-toggle{position:absolute;right:6px;top:50%;transform:translateY(-50%);min-height:38px;padding:6px 12px;font-size:13.5px;font-weight:600;color:var(--brand);border-radius:9px}"),
 # shell
 ("header.top h2{font-size:23px;font-weight:700;letter-spacing:-.015em}",
  "header.top h2{font-size:23px;font-weight:700;letter-spacing:-.02em}"),
 ("nav#tabs{position:fixed;bottom:0;left:0;right:0;background:rgba(255,255,255,.96);backdrop-filter:blur(10px);border-top:1px solid var(--line);display:flex;z-index:50;padding-bottom:env(safe-area-inset-bottom)}",
  "nav#tabs{position:fixed;bottom:0;left:0;right:0;background:rgba(249,248,243,.94);backdrop-filter:blur(14px);border-top:1px solid var(--line);display:flex;z-index:50;padding-bottom:env(safe-area-inset-bottom)}"),
 ("nav#tabs button.active{color:var(--brand)}",
  "nav#tabs button{position:relative}\nnav#tabs button.active{color:var(--brand)}\nnav#tabs button.active::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:26px;height:3px;border-radius:0 0 3px 3px;background:var(--salva)}"),
 # painel
 (".month-picker{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:4px 6px}",
  ".month-picker{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:4px 6px}"),
 (".kpi{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 15px}",
  ".kpi{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 15px}"),
 (".kpi .t{font-size:12px;color:var(--muted);font-weight:600;letter-spacing:.02em}",
  ".kpi .t{font-size:11.5px;color:var(--muted);font-weight:600;letter-spacing:.08em;text-transform:uppercase}"),
 (".kpi.hero{grid-column:span 2;background:linear-gradient(135deg,var(--brand),#3d8563);color:#fff}",
  ".kpi.hero{grid-column:span 2;background:linear-gradient(140deg,#1F2A24 0%,#26332C 55%,#31423A 100%);border-color:#1F2A24;color:var(--on-dark);position:relative;overflow:hidden}\n.kpi.hero::after{content:'';position:absolute;right:-30px;top:-46px;width:150px;height:150px;border-radius:50%;background:rgba(143,174,139,.16)}\n.kpi.hero > *{position:relative;z-index:1}"),
 (".kpi.hero .t,.kpi.hero .s{color:rgba(255,255,255,.85)}",
  ".kpi.hero .t,.kpi.hero .s{color:rgba(247,245,239,.72)}"),
 (".kpi.hero .v.neg{color:#ffd9d4}", ".kpi.hero .v.neg{color:#F0B8AC}"),
 # listas
 (".list-item{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 16px;margin-bottom:9px;display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:64px}",
  ".list-item{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 16px;margin-bottom:9px;display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:64px}"),
 (".list-item.tappable:active{background:#fafbfa}", ".list-item.tappable:active{background:#F2F0E9}"),
 (".badge{display:inline-block;font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:20px}",
  ".badge{display:inline-block;font-size:11.5px;font-weight:600;padding:4px 10px;border-radius:20px;letter-spacing:.01em}"),
 (".badge.pago{background:var(--brand-soft);color:var(--brand-dark)}",
  ".badge.pago{background:var(--ok-soft);color:var(--ok)}"),
 (".badge.chan{background:#eef1ef;color:var(--muted)}",
  ".badge.chan{background:var(--fill);color:var(--muted)}"),
 (".section-title{font-size:16px;font-weight:700;margin:20px 0 10px;letter-spacing:-.01em}",
  ".section-title{font-size:12px;font-weight:600;margin:22px 0 10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}"),
 # forms
 (".item-line{background:#f1f4f1;border-radius:13px;padding:12px;margin-bottom:9px}",
  ".item-line{background:var(--fill);border-radius:var(--radius-sm);padding:12px;margin-bottom:9px}"),
 (".seg{display:flex;background:#e7eae6;border-radius:12px;padding:3px;margin-bottom:14px}",
  ".seg{display:flex;background:var(--fill);border-radius:var(--radius-sm);padding:3px;margin-bottom:14px}"),
 (".seg button.active{background:#fff;color:var(--brand);box-shadow:var(--shadow)}",
  ".seg button.active{background:#fff;color:var(--brand);box-shadow:0 1px 3px rgba(31,42,36,.12)}"),
 # fold / chips
 ("details.fold{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);margin-top:10px;overflow:hidden}",
  "details.fold{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);margin-top:10px;overflow:hidden}"),
 (".chip{display:inline-block;background:#eef1ef;color:var(--muted);border-radius:999px;padding:5px 10px;font-size:12.5px;font-weight:600;margin:0 6px 6px 0}",
  ".chip{display:inline-block;background:var(--fill);color:var(--muted);border-radius:999px;padding:5px 10px;font-size:12.5px;font-weight:600;margin:0 6px 6px 0}"),
 (".bar{height:8px;border-radius:999px;background:#e7eae6;overflow:hidden;margin:10px 0 4px}",
  ".bar{height:8px;border-radius:999px;background:var(--fill);overflow:hidden;margin:10px 0 4px}"),
 (".bar > i{display:block;height:100%;background:var(--brand);border-radius:999px}",
  ".bar > i{display:block;height:100%;background:linear-gradient(90deg,var(--salva),#6E8F6C);border-radius:999px}"),
 (".srow{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:start;gap:4px 10px;padding:10px 0;border-top:1px solid #eceeeb;font-size:13.5px}",
  ".srow{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:start;gap:4px 10px;padding:10px 0;border-top:1px solid var(--line);font-size:13.5px}"),
 (".skel{background:linear-gradient(90deg,#eaede9 25%,#f5f7f4 50%,#eaede9 75%);background-size:200% 100%;animation:sk 1.1s infinite linear;border-radius:var(--radius);height:70px;margin-bottom:10px}",
  ".skel{background:linear-gradient(90deg,#E6E3DA 25%,#F4F2EB 50%,#E6E3DA 75%);background-size:200% 100%;animation:sk 1.1s infinite linear;border-radius:var(--radius);height:70px;margin-bottom:10px}"),
 # dialog / snack
 ("dialog{border:none;border-radius:18px;padding:0;width:min(94vw,480px);box-shadow:0 12px 44px rgba(0,0,0,.28);max-height:88vh;overflow:auto}",
  "dialog{border:none;border-radius:20px;padding:0;width:min(94vw,480px);background:var(--card);box-shadow:var(--shadow-lg);max-height:88vh;overflow:auto}"),
 ("dialog::backdrop{background:rgba(18,28,22,.5)}", "dialog::backdrop{background:rgba(31,42,36,.55);backdrop-filter:blur(2px)}"),
 ("background:#20302a;color:#fff;", "background:var(--pinho);color:var(--on-dark);"),
]
missing=[]
for a,b in REPL:
    if a not in src: missing.append(a[:70])
    src = src.replace(a,b)

# ---------- 6. logótipos ----------
WORD = open('wordmark.svg', encoding='utf-8').read().strip()
ICON = open('icon.svg', encoding='utf-8').read().strip()

old_login = re.search(r'<div class="mark"><svg.*?</svg></div>\s*\n\s*<h1>[^<]*</h1>\s*\n\s*<p>[^<]*</p>', src, re.S)
src = src[:old_login.start()] + (
 '<div class="mark">%s</div>\n    <div class="word">%s</div>\n'
 '    <h1>Gestão</h1>\n    <p>Vendas, stock e finanças num só lugar</p>' % (ICON, WORD)
) + src[old_login.end():]

old_hdr = re.search(r'<span class="brand-mark"><svg.*?</svg></span>', src, re.S)
src = src[:old_hdr.start()] + '<span class="brand-mark">%s</span>' % ICON + src[old_hdr.end():]

# ---------- 7. nomes ----------
src = src.replace('Gestão · Óleos Essenciais','SINNEN')

open('app-v2.html','w',encoding='utf-8').write(src)
print('missing patterns:', missing or 'none')
print('bytes', orig_len, '->', len(src))
