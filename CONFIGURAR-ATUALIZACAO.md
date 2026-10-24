# Configurar a atualização automática

O workflow `.github/workflows/atualizar-dados.yml` roda todo dia às 3h37 (horário de Brasília). Ele baixa a planilha de respostas com uma conta de serviço do Google, limpa os dados com `scripts/limpar_respostas.py` e grava só `docs/dados/respostas.csv` no repositório. O GitHub Pages republica o site sozinho em seguida.

A configuração é feita uma vez só e leva uns 15 minutos.

## 1. Criar a conta de serviço no Google Cloud

1. Acesse https://console.cloud.google.com e entre com sua conta Google.
2. No seletor de projetos, no alto da página, clique em **Novo projeto**. Use o nome `painel-mestrados-iffar` e clique em **Criar**.
3. Com o projeto selecionado, abra **APIs e serviços > Biblioteca**, procure **Google Drive API** e clique em **Ativar**.
4. Abra **IAM e administrador > Contas de serviço** e clique em **Criar conta de serviço**.
   - Nome: `leitor-planilha`.
   - Clique em **Criar e continuar**, pule a parte de papéis e clique em **Concluir**. A conta não precisa de nenhum papel no projeto.
5. Clique na conta criada e copie o e-mail dela. Ele termina em `@painel-mestrados-iffar.iam.gserviceaccount.com`.
6. Abra https://console.cloud.google.com/iam-admin/serviceaccounts, com o projeto `painel-mestrados-iffar` selecionado no alto da página, e clique no e-mail da conta `leitor-planilha` (é um link azul na lista). Na página da conta, as abas ficam logo abaixo do título: **Detalhes**, **Permissões**, **Chaves** (em inglês, **Keys**), **Métricas** e **Registros**. Na aba **Chaves**, clique em **Adicionar chave > Criar nova chave**, escolha **JSON** e clique em **Criar**. Um arquivo `.json` é baixado.

Esse arquivo é a senha da conta de serviço. Não o envie por e-mail nem o coloque na pasta do projeto.

**Se a criação da chave for bloqueada:** contas institucionais às vezes têm uma política que proíbe chaves de conta de serviço. Nesse caso, crie o projeto com uma conta Google pessoal (Gmail).

## 2. Compartilhar a planilha com a conta de serviço

1. Abra a planilha de respostas no Google Sheets.
2. Clique em **Compartilhar** e cole o e-mail da conta de serviço.
3. Escolha **Leitor**, desmarque **Notificar pessoas** e clique em **Compartilhar**.

**Se aparecer um aviso de que não é permitido compartilhar fora da organização:** o Google Workspace do IFFar bloqueia compartilhamento externo. Peça à TI do IFFar uma exceção para esse e-mail, ou use a atualização pelo computador no lugar desta.

## 3. Guardar os segredos no GitHub

No repositório do GitHub, abra **Settings > Secrets and variables > Actions** e clique em **New repository secret** duas vezes:

| Nome | Valor |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | O conteúdo inteiro do arquivo `.json` baixado no passo 1. Abra o arquivo no Bloco de Notas, copie tudo e cole. |
| `PLANILHA_ID` | O id da planilha: o trecho da URL entre `/d/` e `/edit`. |

Os segredos não aparecem no repositório nem nos registros das execuções. Depois de salvá-los, apague o arquivo `.json` do computador.

## 4. Permitir que o workflow grave no repositório

Em **Settings > Actions > General**, na seção **Workflow permissions**, marque **Read and write permissions** e clique em **Save**.

## 5. Ativar o GitHub Pages

Em **Settings > Pages**, escolha **Deploy from a branch**, a branch `main` e a pasta `/docs`, e clique em **Save**. Em um ou dois minutos o endereço aparece no alto da página.

## 6. Testar

1. Abra a aba **Actions**, escolha **Atualizar dados do painel** e clique em **Run workflow**.
2. Em cerca de um minuto, a execução deve ficar verde.
   - Se houver respostas novas, aparece um commit "Atualiza respostas do estudo de demanda".
   - Se não houver, o registro diz "Nenhuma resposta nova".
3. Se ficar vermelha, abra a execução e leia a última mensagem:

| Mensagem | O que fazer |
|---|---|
| "A conta de serviço não conseguiu abrir a planilha" | Refaça o passo 2 com o e-mail exato da conta de serviço. |
| "Defina GOOGLE_SERVICE_ACCOUNT_JSON e PLANILHA_ID" | Confira os nomes dos segredos no passo 3. |
| "Coluna não encontrada na planilha" | Uma pergunta do formulário foi renomeada. Ajuste a lista `COLUNAS` em `scripts/limpar_respostas.py`. |
| "Permission denied" no `git push` | Refaça o passo 4. |

## Bom saber

- **Formulário fechado:** quando o formulário fechar, desative o workflow em **Actions > Atualizar dados do painel > ⋯ > Disable workflow**.
- **Repositório sem movimento:** o GitHub pausa agendamentos de repositórios sem nenhuma atividade por 60 dias. Os commits diários do próprio workflow contam como atividade enquanto chegarem respostas novas.
- **Painel do Claude:** a tarefa agendada no computador continua atualizando o painel do Claude. As duas atualizações são independentes.
