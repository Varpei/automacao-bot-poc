# Assistente de atendimento via WhatsApp

Template de uma POC para automatizar atendimento por WhatsApp com Evolution API, n8n, PostgreSQL, Redis e um modelo de IA local. O projeto pode ser adaptado para outros canais, organizações e regras de negócio.

> **Escopo:** esta é uma base de desenvolvimento local, não uma implantação pronta para produção. Segredos, configurações privadas, documentação operacional interna e dados reais não fazem parte da publicação.

## Arquitetura

```text
WhatsApp
   │
   ▼
Adaptador de mensagens (Evolution API na POC)
   │
   ▼
n8n ───────────► API de IA local (Ollama ou endpoint compatível)
   │
   └────────────► resposta pelo adaptador de mensagens

PostgreSQL e Redis fornecem persistência e estado do adaptador.
```

O `docker-compose.yml` executa n8n, Evolution API, PostgreSQL e Redis. O modelo de IA é executado fora do Compose e acessado pelo n8n. O workflow está em `workflow-receber-mensagem.json`.

## O que é publicado

O repositório público deve conter apenas código e configuração genérica:

```text
docker-compose.yml
workflow-receber-mensagem.json
*.sh
*.py
README.md
.env.example
.gitignore
```

Os seguintes itens são deliberadamente excluídos:

- `.env` e qualquer outro arquivo `.env.*` com exceção de `.env.example`;
- `docs/`, que contém documentação operacional privada;
- QR Codes, logs, caches, backups, dumps e dados de mensagens.

O `.gitignore` protege esses caminhos para novos commits. Se algum segredo já tiver sido commitado no passado, ele deve ser revogado e removido do histórico Git; apenas adicioná-lo ao `.gitignore` não é suficiente.

## Requisitos

- Docker Engine e Docker Compose v2;
- Python 3.9 ou superior;
- `curl`;
- um servidor de IA local compatível com o workflow;
- portas livres para n8n e o adaptador de mensagens;
- um canal e números de teste autorizados.

## Configuração local

```bash
cp .env.example .env
```

Edite `.env` e preencha:

| Variável | Finalidade |
| --- | --- |
| `EVOLUTION_API_KEY` | Chave da instância local da Evolution API |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL |
| `WHATSAPP_CLIENT_NAME` | Nome da instância/canal |
| `OLLAMA_BASE_URL` | Endereço da IA acessível pelo n8n |
| `OLLAMA_MODEL` | Modelo aprovado e instalado |
| `N8N_WEBHOOK_URL` | URL anunciada pelo n8n |
| `EVOLUTION_WEBHOOK_URL` | URL do webhook resolvível pelo adaptador |

Gere segredos locais, por exemplo:

```bash
openssl rand -hex 32
```

Não use chaves de exemplo em homologação ou produção. A integração com outro gateway, como uma plataforma institucional, exige adaptar autenticação, endpoints, eventos e payloads; não basta trocar a chave.

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
5. crie a instância do canal;
6. configure e verifique o webhook;
7. execute testes apenas com dados sintéticos.

## Scripts

Execute da raiz do projeto:

| Arquivo | Função |
| --- | --- |
| `conectar.sh` | Cria a instância do adaptador e solicita QR Code |
| `conectar-pratico.py` | Solicita o QR Code e salva `qrcode.png` localmente |
| `diagnostico.py` | Consulta o estado da conexão |
| `verificar-webhook.py` | Consulta o webhook configurado |
| `definir-webhook.py` | Configura o webhook |
| `configurar-webhook.sh` | Alternativa shell para configurar o webhook |
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

O evento de entrada esperado contém um identificador como `data.key.remoteJid` e texto em `data.message.conversation` ou em uma mensagem de texto estendida. A implementação deve validar campos obrigatórios, normalizar o destinatário e tratar entradas inválidas sem enviar para um destino vazio.

O prompt é uma referência. Substitua escopo, idioma, menu, dados mínimos, encaminhamento humano e regras de negócio para cada implantação. A IA não substitui autenticação, autorização, validação de negócio ou aprovação humana.

## IA local

O projeto suporta duas formas de integração:

- API nativa do servidor local, como `/api/chat`;
- API compatível com OpenAI, como `/v1/chat/completions`.

Escolha CPU/GPU, modelo, endpoint, timeout, limite de contexto e política de atualização conforme o ambiente. Para RAG, embeddings e armazenamento vetorial devem ser projetados separadamente; não estão implementados neste template.

## Operação

```bash
docker compose --env-file .env ps
docker compose --env-file .env logs --tail=100 n8n evolution-api
docker compose --env-file .env stop
docker compose --env-file .env start
```

Não use `docker compose down -v` como rotina: ele remove volumes e pode apagar configurações, banco e sessão do canal. Faça backup e tenha rollback antes de atualizar imagens ou modelos. Fixe versões em ambientes controlados; `latest` é apenas para experimentação.

## Segurança e transferência

- nunca publique tokens, chaves, QR Codes, certificados privados, mensagens reais ou dumps;
- use `.env`, secrets ou cofre corporativo;
- prefira HTTPS, autenticação do webhook, rede segmentada e menor privilégio;
- não desabilite validação TLS para contornar erro de certificado em produção;
- defina retenção, backup, logs sem dados pessoais, monitoramento e responsáveis;
- valide LGPD, licenças, política do canal e aprovação de segurança;
- homologue em ambiente separado antes de produção;
- documente DNS, firewall, proxy, certificados, recursos de CPU/RAM/GPU e rollback em documentação privada.

## Verificação antes de publicar

```bash
git status --short
git check-ignore -v .env .env.documentation docs/
git grep -n -E 'tre_go_secret|tre_pass|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key[[:space:]]*[:=]' -- ':!README.md' ':!.env.example' || true
```

O resultado esperado é que `.env`, `.env.documentation` e `docs/` sejam ignorados e que a busca não encontre credenciais ou chaves privadas nos arquivos públicos. Revise também manualmente o workflow antes do primeiro `git push`.
