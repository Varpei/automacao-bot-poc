#!/usr/bin/env bash
set -euo pipefail
set -a
source ./.env
set +a

# Cria uma instância da Evolution API para a POC local.
# O método POST solicita a criação do recurso no endpoint da Evolution API.
# O header Content-Type informa que o payload está em JSON, enquanto o header
# apikey autentica a chamada com a chave configurada no serviço.
# O payload define o nome da instância, solicita a geração do QR Code e escolhe
# a integração WhatsApp Baileys usada para conectar o telefone.
curl --fail-with-body --request POST \
  --url "${EVOLUTION_SERVER_URL}/instance/create" \
  --header "Content-Type: application/json" \
  --header "apikey: ${EVOLUTION_API_KEY}" \
  --data '{
    "instanceName": "'"${WHATSAPP_CLIENT_NAME}"'",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'
