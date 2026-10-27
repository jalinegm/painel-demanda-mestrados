"""Monta o site estático do painel (docs/) a partir de src/painel.html.

src/painel.html é a mesma página usada no painel do Claude (Artifact do tipo
Dashboard). Aqui ela ganha um documento HTML completo e uma pequena versão do
objeto `dash` que lê docs/dados/respostas.csv, para rodar em qualquer
hospedagem estática, como o GitHub Pages.

Uso: python -I scripts/montar_site.py
"""
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "src"
DOCS = RAIZ / "docs"

CABECALHO = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mestrados Profissionais IFFar · Estudo de Demanda</title>
<meta name="description" content="Resultados do estudo de demanda dos mestrados profissionais do IFFar: quantas pessoas querem cursar, de onde vêm e o que disseram.">
<meta property="og:title" content="Mestrados Profissionais IFFar · Estudo de Demanda">
<meta property="og:description" content="Quantas pessoas querem cursar os mestrados profissionais propostos pelo IFFar, de onde vêm e o que disseram.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0e3b22">
<style>
:root {
  --font-anthropic-sans: system-ui, -apple-system, "Segoe UI", sans-serif;
  --cds-ease-out: cubic-bezier(.16, 1, .3, 1);
  --cds-dur-slow: .3s;
  --color-bad: #ff8a80;
}
html, body { margin: 0; background: #0e3b22; }
.dash-skeleton { color: transparent !important; background: rgba(255, 255, 255, .12); border-radius: 4px; }
.mp-rows.dash-skeleton { min-height: 8rem; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
// Versão mínima do objeto `dash` do painel do Claude, lendo o CSV publicado ao lado.
(() => {
  const calcs = {};
  const inscritos = [];
  const CURSOS = ['todos', 'ensino', 'ambientais'];
  const inicial = location.hash.slice(1);
  let params = { curso: CURSOS.includes(inicial) ? inicial : 'todos' };
  let estado = 'loading';
  let linhas = [];
  let conferidoEm = null;
  const rodar = () => inscritos.forEach((fn) => fn());
  fetch('dados/atualizacao.json', { cache: 'no-cache' })
    .then((r) => (r.ok ? r.json() : null))
    .then((j) => { if (j && j.conferido_em) { conferidoEm = j.conferido_em; rodar(); } })
    .catch(() => {});
  fetch('dados/respostas.csv', { cache: 'no-cache' })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then((texto) => { linhas = d3.csvParse(texto); estado = 'ok'; rodar(); })
    .catch(() => { estado = 'error'; rodar(); });
  window.dash = {
    calc: (id, def) => { calcs[id] = def; },
    data: (id) => {
      if (estado !== 'ok') return { status: estado, data: [] };
      if (id === 'respostas') return { status: 'ok', data: linhas };
      const c = calcs[id];
      if (!c) return { status: 'missing', data: [] };
      if (!c.resultado) c.resultado = c.fn(...c.inputs.map(() => linhas));
      return { status: 'ok', data: c.resultado };
    },
    onData: (fn) => { inscritos.push(fn); fn(); },
    params: () => params,
    setParams: (p) => {
      params = { ...params, ...p };
      try { history.replaceState(null, '', params.curso === 'todos' ? location.pathname : '#' + params.curso); } catch (e) {}
      rodar();
    },
    resetParams: () => { params = { curso: 'todos' }; rodar(); },
    setLink: () => {},
    // Só no site estático: quando o GitHub Actions conferiu a planilha pela última vez.
    conferidoEm: () => conferidoEm,
    refresh: () => {},
    colors: []
  };
})();
</script>
</head>
<body>
<div id="dash-root">
"""

RODAPE = """
</div>
</body>
</html>
"""


def main():
    DOCS.mkdir(exist_ok=True)
    pagina = (SRC / "painel.html").read_text(encoding="utf-8")
    (DOCS / "index.html").write_text(CABECALHO + pagina + RODAPE, encoding="utf-8")
    shutil.copyfile(SRC / "poppins.css", DOCS / "poppins.css")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Site montado em {DOCS}")


if __name__ == "__main__":
    main()
