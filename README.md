# SINNEN

App de gestão da SINNEN — revenda de óleos essenciais e difusores doTERRA.
Controlo de encomendas, stock por lote, custos (produto, embalagem, brindes),
autoconsumo, preços com desconto por volume e distribuição de lucros entre sócios.

Uma única página HTML, mobile-first, em português, com Supabase (Postgres + Auth
+ RLS) como backend. Sem framework, sem passo de compilação de JS: o `build.py`
apenas embute a biblioteca do Supabase dentro do HTML para o ficheiro funcionar
mesmo aberto directamente do disco (`file://`) ou servido como estático.

## Estrutura

```
src/app.html      fonte editável — é aqui que se mexe
build.py          gera dist/ a partir de src/
dist/             o que é publicado (index.html, 200.html, _redirects, _headers)
brand/            símbolo, wordmark, ícone e as fontes Poppins (woff2)
tools/            scripts auxiliares (rebrand, contraste, fixtures)
test/             harness Playwright + fixtures de dados falsos
docs/             documentação do modelo de distribuição de lucros
```

## Como construir

```bash
npm install
python3 build.py       # escreve dist/index.html e dist/200.html
```

O `build.py` substitui a tag `<script src="…supabase-js@2">` pelo bundle UMD
inteiro. O resultado ronda os 330 KB e não depende de nenhum CDN.

## Como testar

```bash
node test/test-v2.mjs
```

O harness abre o `dist/index.html` num Chromium headless, intercepta as chamadas
PostgREST e responde a partir de `test/fixtures.json` com um mini-motor de
filtros. Percorre os 11 ecrãs, grava capturas em `test/shots/` e imprime
`{"errors":[]}` quando tudo passa. Não toca na base de dados real.

Para regenerar os dados falsos: `python3 tools/gen_fixtures.py`.

## Marca

Paleta e tipografia vivem no bloco `:root` de `src/app.html`, como tokens
semânticos. As cores da marca são Pinho `#1F2A24`, Salva `#8FAE8B`, Linho
`#F7F5EF` e Lavanda `#B7A6D4`; os tokens de superfície, texto, acção e estado
derivam daí. A tipografia é Poppins, embutida em base64 a partir de
`brand/fonts/` (subconjunto latino, cinco pesos).

O Salva é uma cor decorativa: barras de progresso, anel de foco, indicador do
separador activo. Nunca é usado como texto — o contraste sobre superfície clara
é 2.30, abaixo do mínimo. Todos os pares texto/fundo em uso passam WCAG AA
(≥ 4.5). Para reauditar depois de mexer nas cores:

```bash
python3 tools/contrast.py
```

O `tools/rebrand.py` é o script que aplicou a identidade ao HTML original.
Fica no repositório como registo da transformação; não é preciso correr outra vez.

## Backend

Projecto Supabase `zpfvpfbitejjwsmycsbl` (eu-west-1).
A chave publicável está embutida no HTML — é pública por design e a segurança
está toda em Row Level Security.

Todas as tabelas `oleos_*` são protegidas pela função `SECURITY DEFINER`
`oleos_is_socio()`, que confirma que o utilizador autenticado existe em
`oleos_socios` com `acesso = true`. O mesmo se aplica ao bucket `app` no
Storage. Quem não for sócio não lê nem escreve nada.

Os lotes guardam o capital investido e a divisão de lucro em mapas `jsonb`
indexados pelo **id estável do sócio** (nunca pelo email, que pode mudar). A
atribuição das unidades vendidas aos lotes é FIFO e calculada no cliente
(`calcLotes()`), o que permite margens diferentes por lote e por sócio.

## Publicar

`dist/` é um site estático — serve em qualquer alojamento de ficheiros.
Já traz `200.html` (fallback de SPA), `_redirects` e `_headers` com
X-Frame-Options, X-Content-Type-Options e Referrer-Policy.

Nota: o Supabase Storage **não** serve HTML — devolve sempre `text/plain`,
mesmo com o mimetype correcto guardado. As Edge Functions são reescritas da
mesma forma pelo gateway. Esse caminho está fechado; usar Netlify, Cloudflare
Pages, GitHub Pages ou equivalente.

## Publicar no GitHub

O repositório está inicializado localmente. Para o enviar:

```bash
git remote add origin git@github.com:<utilizador>/sinnen.git
git push -u origin main
```
