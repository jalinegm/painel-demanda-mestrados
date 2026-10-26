# Estudo de Demanda: Mestrados Profissionais IFFar

Painel com os resultados do formulário de interesse nos mestrados profissionais propostos pelo IFFar:

- Mestrado Profissional em Ensino e Tecnologias (Campus Alegrete)
- Mestrado Profissional em Ciências Ambientais e Sistemas Produtivos (Campi Alegrete, Júlio de Castilhos e Panambi)

O painel serve para mostrar às equipes das propostas (APCN) e à gestão do IFFar que a demanda existe: quantas pessoas querem cursar, de onde vêm, quando entrariam e o que escreveram. Ele tem um filtro por curso, e cada curso tem um link próprio (`#ensino`, `#ambientais`).

## Estrutura

| Pasta ou arquivo | O que é |
|---|---|
| `src/painel.html` | A página do painel. É a mesma página publicada no painel do Claude. |
| `src/poppins.css` | Fonte Poppins embutida (pesos 500 a 900). |
| `scripts/baixar_planilha.py` | Baixa a aba de respostas com uma conta de serviço do Google (usado pelo GitHub Actions). |
| `.github/workflows/atualizar-dados.yml` | Atualização diária automática dos dados. |
| `scripts/limpar_respostas.py` | Limpa a exportação da planilha: tira as colunas de e-mail e remove e-mails e telefones escritos nos comentários. |
| `scripts/montar_site.py` | Gera o site estático em `docs/` a partir de `src/`. |
| `docs/` | O site pronto para o GitHub Pages. `docs/dados/respostas.csv` são as respostas já limpas. |
| `marca/` | Marca do IFFar usada na página e a origem dela (`ORIGEM.md`). |
| `fontes/` | Arquivos originais da Poppins (licença SIL Open Font License 1.1). |
| `PRODUCT.md`, `.impeccable/` | Contexto do produto e decisões de design. |

## Atualizar os dados

O GitHub Actions confere a planilha a cada 3 horas e grava os dados quando há respostas novas. Veja [CONFIGURAR-ATUALIZACAO.md](CONFIGURAR-ATUALIZACAO.md) para a configuração inicial.

Para atualizar à mão:

1. Exporte a planilha de respostas como CSV, ou use o arquivo baixado pelo Google Drive.
2. Limpe e grave em `docs/dados/`:

   ```bash
   python -I scripts/limpar_respostas.py respostas-brutas.csv docs/dados/respostas.csv
   ```

3. Nunca faça commit do arquivo bruto: ele tem os e-mails de quem respondeu.

Depois de mudar `src/painel.html`, monte o site de novo:

```bash
python -I scripts/montar_site.py
```

## Ver localmente

```bash
python -m http.server 8000 --directory docs
```

Depois abra http://localhost:8000.

## Publicar no GitHub Pages

1. Crie o repositório no GitHub e envie esta pasta.
2. Em **Settings > Pages**, escolha **Deploy from a branch**, a branch `main` e a pasta `/docs`.
3. O endereço fica no formato `https://<usuario>.github.io/<repositorio>/`.

Atenção: no plano gratuito, o GitHub Pages só funciona com repositório público. Assim, qualquer pessoa pode ver o código e o `docs/dados/respostas.csv`, inclusive o histórico de versões. O arquivo não tem e-mails nem telefones, mas tem os comentários, os municípios e os nomes e cargos de quem respondeu pelas instituições. Contas com GitHub Pro (gratuito para professores pelo GitHub Education) podem publicar a partir de um repositório privado, mas o site em si continua público.
