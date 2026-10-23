"""Baixa a aba de respostas da planilha como CSV, usando uma conta de serviço do Google.

Uso: python -I scripts/baixar_planilha.py <saida.csv>

Variáveis de ambiente:
  GOOGLE_SERVICE_ACCOUNT_JSON  conteúdo do arquivo JSON da chave da conta de serviço
  PLANILHA_ID                  id da planilha (o trecho entre /d/ e /edit na URL)
  PLANILHA_GID                 gid da aba de respostas (padrão: 902475231)

O arquivo baixado tem os e-mails de quem respondeu: ele só existe durante a
execução e nunca deve ser versionado. Passe-o direto para limpar_respostas.py.
"""
import json
import os
import sys

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

ESCOPOS = ["https://www.googleapis.com/auth/drive.readonly"]


def main(saida):
    chave = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    planilha = os.environ.get("PLANILHA_ID")
    aba = os.environ.get("PLANILHA_GID", "902475231")
    if not chave or not planilha:
        sys.exit("Defina GOOGLE_SERVICE_ACCOUNT_JSON e PLANILHA_ID.")

    credenciais = service_account.Credentials.from_service_account_info(json.loads(chave), scopes=ESCOPOS)
    sessao = AuthorizedSession(credenciais)
    url = f"https://docs.google.com/spreadsheets/d/{planilha}/export?format=csv&gid={aba}"
    resposta = sessao.get(url, timeout=60)
    if resposta.status_code in (401, 403, 404):
        sys.exit(
            f"A conta de serviço não conseguiu abrir a planilha (HTTP {resposta.status_code}). "
            "Confira se a planilha foi compartilhada com o e-mail da conta de serviço como Leitor."
        )
    resposta.raise_for_status()
    if "text/csv" not in resposta.headers.get("Content-Type", ""):
        sys.exit("O Google não devolveu um CSV. Confira PLANILHA_ID e PLANILHA_GID.")

    with open(saida, "wb") as f:
        f.write(resposta.content)
    print(f"Planilha baixada ({len(resposta.content)} bytes).")


if __name__ == "__main__":
    main(sys.argv[1])
