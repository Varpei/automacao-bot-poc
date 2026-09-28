#!/usr/bin/env bash
set -euo pipefail
set -a
source ./.env
set +a
# Configura o Webhook na Evolution API para enviar mensagens ao n8n

# O método POST atualiza a configuração do webhook da instância configurada.
# Content-Type indica que o corpo é JSON e apikey autoriza a alteração na API.
# O payload habilita o webhook, aponta para a rota interna do n8n e limita os
# eventos encaminhados a MESSAGES_UPSERT, sem transportar conteúdo em Base64.
curl --fail-with-body --request POST \
  --url "${EVOLUTION_SERVER_URL}/webhook/set/${WHATSAPP_CLIENT_NAME}" \
  --header "Content-Type: application/json" \
  --header "apikey: ${EVOLUTION_API_KEY}" \
  --data '{
    "webhook": {
      "enabled": true,
      "url": "'"${EVOLUTION_WEBHOOK_URL}"'",
      "byEvents": false,
      "base64": false,
      "events": [
        "MESSAGES_UPSERT",
        "CONNECTION_UPDATE"
      ]
    }
  }'
