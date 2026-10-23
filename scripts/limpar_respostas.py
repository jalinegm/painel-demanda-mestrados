"""Limpa a exportação da planilha de respostas dos mestrados profissionais IFFar
para o painel compartilhado.

Uso: python -I limpar_respostas.py <entrada> <saida.csv>

<entrada> pode ser o CSV exportado da planilha ou o JSON salvo pela ferramenta
download_file_content do Google Drive ({"content": <base64 ou texto>, ...}).

Nunca grava as colunas de e-mail. Remove e-mails e telefones escritos em campos
de texto livre. Múltipla escolha sai separada por "; ".
"""
import base64
import csv
import io
import json
import re
import sys
from datetime import datetime

# coluna no painel -> início do cabeçalho na planilha
COLUNAS = [
    ("carimbo", "Timestamp"),
    ("vinculo", "Qual é o seu vínculo com o IFFar"),
    ("nivel", "Em qual nível de ensino"),
    ("unidades", "Com quais unidades do IFFar"),
    ("municipio", "Qual é o município onde você reside"),
    ("uf", "UF"),
    ("perfil", "Qual(is) opção(ões) descreve(m) seu perfil"),
    ("curso_interesse", "Qual dos cursos de mestrado profissional propostos"),
    ("contextos", "Em quais contextos você pretende aplicar"),
    ("horizonte", "Em que horizonte você consideraria"),
    ("periodos", "Quais períodos seriam mais adequados"),
    ("municipios_disponiveis", "Em quais destes municípios"),
    ("curso_sugerido", "Qual curso de mestrado profissional você gostaria de sugerir"),
    ("inst_tipo", "Qual tipo de instituição"),
    ("inst_nome", "Qual é o nome da instituição"),
    ("inst_cargo", "Qual é o seu vínculo ou cargo na instituição"),
    ("inst_municipio", "Em qual município está localizada a instituição"),
    ("inst_uf", "UF da instituição"),
    ("inst_incentivar", "Qual seria o interesse da instituição que você representa nas seguintes formas de colaboração com os cursos de mestrado propostos pelo IFFar? [Incentivar"),
    ("inst_parcerias", "Qual seria o interesse da instituição que você representa nas seguintes formas de colaboração com os cursos de mestrado propostos pelo IFFar? [Estabelecer"),
    ("inst_programas", "Em qual(is) possível(is) programa(s)"),
    ("quer_informacoes", "Você gostaria de receber informações"),
    ("curso_iffar", "Qual curso?"),
    ("comentario", "Algum comentário para o IFFar"),
]
MULTIPLA = {"unidades", "perfil", "contextos", "periodos", "municipios_disponiveis", "inst_programas"}
LIVRE = {"municipio", "curso_sugerido", "inst_nome", "inst_cargo", "inst_municipio", "curso_iffar", "comentario"}

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
TELEFONE = re.compile(r"\(?\d[\d\s().-]{7,}\d")


def ler_entrada(caminho):
    texto = open(caminho, encoding="utf-8-sig").read()
    if texto.lstrip().startswith("{"):
        conteudo = json.loads(texto)["content"]
        try:
            return base64.b64decode(conteudo, validate=True).decode("utf-8-sig")
        except Exception:
            return conteudo
    return texto


def carimbo_iso(valor):
    # A exportação segue a localidade da planilha: 10/23/2026 12:24:42 ou 23/10/2026 12:24:42.
    for formato in ("%m/%d/%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(valor, formato).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass
    sys.exit(f"Data em formato desconhecido na coluna Timestamp: {valor}")


def separar(valor):
    # Opções do Forms começam com maiúscula; pedaço em minúscula continua a opção anterior.
    partes = []
    for p in (x.strip() for x in valor.split(", ")):
        if not p:
            continue
        if partes and p[0].islower():
            partes[-1] += ", " + p
        else:
            partes.append(p)
    return "; ".join(partes)


def limpar(valor):
    valor = re.sub(r"\s+", " ", valor)
    valor = EMAIL.sub("[e-mail removido]", valor)
    return TELEFONE.sub("[telefone removido]", valor).strip()


def main(entrada, saida):
    linhas = list(csv.reader(io.StringIO(ler_entrada(entrada))))
    cabecalho, dados = linhas[0], linhas[1:]
    indices = {}
    for nome, inicio in COLUNAS:
        achados = [i for i, h in enumerate(cabecalho) if h.strip() == inicio or h.strip().startswith(inicio) and nome != "uf"]
        if not achados:
            sys.exit(f"Coluna não encontrada na planilha: {inicio}")
        indices[nome] = achados[0]
    if any("mail" in cabecalho[i].lower() for i in indices.values()):
        sys.exit("Uma coluna de e-mail foi mapeada por engano; nada foi gravado.")

    with open(saida, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id"] + [n for n, _ in COLUNAS])
        n = 0
        for r in dados:
            if not any(c.strip() for c in r):
                continue
            n += 1
            saida_linha = [n]
            for nome, _ in COLUNAS:
                i = indices[nome]
                v = r[i].strip() if i < len(r) else ""
                if nome == "carimbo" and v:
                    v = carimbo_iso(v)
                elif nome in MULTIPLA:
                    v = separar(v)
                elif nome in LIVRE:
                    v = limpar(v)
                saida_linha.append(v)
            w.writerow(saida_linha)

    if "@" in open(saida, encoding="utf-8").read():
        sys.exit("Ainda há um @ no arquivo limpo; não envie.")
    print(f"{n} respostas gravadas em {saida}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
