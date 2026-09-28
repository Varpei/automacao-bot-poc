# Template de bot de atendimento via WhatsApp

Template de uma POC para iniciar um bot de atendimento via WhatsApp. A integração de referência usa n8n, um adaptador de mensagens, persistência opcional e um serviço de IA. O projeto foi estruturado para que o adaptador, o provedor de IA, as regras de negócio e os serviços de apoio possam ser substituídos conforme o caso de uso.

> **Escopo:** esta é uma base de desenvolvimento local, não uma implantação pronta para produção. Segredos, configurações privadas, documentação operacional interna e dados reais não fazem parte da publicação.

## Arquitetura

```text
WhatsApp
   │
   ▼
Adaptador de mensagens (implementação de referência)
   │
   ▼
n8n ───────────► API de IA local (Ollama ou endpoint compatível)
   │
   └────────────► resposta pelo adaptador de mensagens

PostgreSQL e Redis fornecem persistência e estado do adaptador.
```

O `docker-compose.yml` traz uma implementação de referência com n8n, Evolution API, PostgreSQL e Redis. Essa composição pode ser substituída ou reduzida quando outro gateway, banco, fila ou serviço de IA for adotado. O modelo de IA é executado fora do Compose e acessado pelo n8n. O workflow está em `workflow-receber-mensagem.json`.

## O que é publicado

O repositório público deve conter apenas código e configuração genérica:

```text
docker-compose.yml
workflow-receber-mensagem.json
*.sh
*.py
README.md
.env.example
.env.documentation
.gitignore
```

Os seguintes itens são deliberadamente excluídos:

- `.env` e qualquer outro arquivo `.env.*` com exceção de `.env.example` e `.env.documentation`;
- `docs/`, que contém documentação operacional privada;
- QR Codes, logs, caches, backups, dumps e dados de mensagens.

O `.gitignore` protege esses caminhos para novos commits. Se algum segredo já tiver sido commitado no passado, ele deve ser revogado e removido do histórico Git; apenas adicioná-lo ao `.gitignore` não é suficiente.

## Requisitos

- Docker Engine e Docker Compose v2;
- Python 3.9 ou superior;
- `curl`;
- um servidor de IA local compatível com o workflow;
- portas livres para n8n e o adaptador de mensagens escolhido;
- um canal e números de teste autorizados.

## Configuração local

```bash
cp .env.example .env
```

Edite `.env` e preencha:

| Variável | Finalidade |
| --- | --- |
| `EVOLUTION_API_KEY` | Chave do adaptador de referência, se utilizado |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL |
| `WHATSAPP_CLIENT_NAME` | Nome da instância/canal |
| `OLLAMA_BASE_URL` | Endereço da IA acessível pelo n8n |
| `OLLAMA_MODEL` | Modelo aprovado e instalado |
| `N8N_WEBHOOK_URL` | URL anunciada pelo n8n |
| `EVOLUTION_WEBHOOK_URL` | URL do webhook resolvível pelo adaptador de referência |

Gere segredos locais, por exemplo:

```bash
openssl rand -hex 32
```

Não use chaves de exemplo em homologação ou produção. A integração com outro gateway exige adaptar autenticação, endpoints, eventos e payloads; não basta trocar a chave.

## Inicialização

```bash
docker compose --env-file .env config --quiet
docker compose --env-file .env up -d
docker compose --env-file .env ps
```

Instale e inicie o servidor de IA escolhido. Para Ollama:

```bash
ollama pull <modelo>
ollama serve
```

Depois:

1. acesse o n8n pelo endereço configurado;
2. crie o usuário administrador;
3. importe `workflow-receber-mensagem.json`;
4. revise URL, modelo, prompt e credenciais;
5. configure o canal ou adaptador escolhido;
6. configure e verifique o webhook;
7. execute testes apenas com dados sintéticos.

## Scripts

Execute da raiz do projeto:

| Arquivo | Função |
| --- | --- |
| `conectar.sh` | Cria uma instância no adaptador de referência e solicita QR Code |
| `conectar-pratico.py` | Solicita o QR Code do adaptador de referência e salva `qrcode.png` localmente |
| `diagnostico.py` | Consulta o estado da conexão no adaptador de referência |
| `verificar-webhook.py` | Consulta o webhook configurado no adaptador de referência |
| `definir-webhook.py` | Configura o webhook no adaptador de referência |
| `configurar-webhook.sh` | Alternativa shell para configurar o webhook de referência |
| `auditoria-geral.py` | Verifica os serviços locais |
| `debug-docker.sh` | Exibe o contêiner e logs do adaptador |
| `testes-seguranca.sh` | Testa fluxo normal, payload inválido e prompt injection |

```bash
chmod +x *.sh
python3 auditoria-geral.py
./testes-seguranca.sh
```

Os scripts exigem que `.env` esteja carregado no ambiente. Não execute criação de instância, pareamento ou testes contra sistemas de terceiros sem autorização.

## Workflow e contrato de mensagens

O workflow possui três etapas:

1. webhook `POST` para receber eventos;
2. chamada à IA para gerar a resposta;
3. chamada ao adaptador para enviar a resposta ao remetente.

O workflow de referência espera um evento com um identificador como `data.key.remoteJid` e texto em `data.message.conversation` ou em uma mensagem de texto estendida. Ao trocar o adaptador, adapte o contrato de entrada e saída. Em qualquer integração, valide campos obrigatórios, normalize o destinatário e trate entradas inválidas sem enviar para um destino vazio.

O prompt é uma referência. Substitua escopo, idioma, menu, dados mínimos, encaminhamento humano e regras de negócio para cada implantação. A IA não substitui autenticação, autorização, validação de negócio ou aprovação humana.

## Integração com IA

O template pode ser conectado a diferentes servidores ou provedores de IA:

- API nativa do provedor escolhido, como `/api/chat`;
- API compatível com OpenAI, como `/v1/chat/completions`.

Escolha o provedor, modelo, endpoint, timeout, limite de contexto e política de atualização conforme o ambiente. CPU, GPU, execução local ou serviço remoto são decisões de implantação. Para RAG, embeddings e armazenamento vetorial devem ser projetados separadamente; não estão implementados neste template.

## Operação

```bash
docker compose --env-file .env ps
docker compose --env-file .env logs --tail=100 n8n evolution-api
docker compose --env-file .env stop
docker compose --env-file .env start
```

Não use `docker compose down -v` como rotina: ele remove volumes e pode apagar configurações, banco e sessão do canal. Faça backup e tenha rollback antes de atualizar imagens ou modelos. Fixe versões em ambientes controlados; `latest` é apenas para experimentação.
