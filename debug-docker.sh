#!/usr/bin/env bash
set -euo pipefail
set -a
source ./.env
set +a

# Exibe o estado atual do contêiner da Evolution API.
echo "=== Status do contêiner ${EVOLUTION_CONTAINER_NAME} ==="
docker ps -a | grep "${EVOLUTION_CONTAINER_NAME}" || true

# Exibe as últimas 30 linhas de log para identificar falhas de inicialização.
echo
echo "=== Últimas 30 linhas de log ==="
docker logs --tail 30 "${EVOLUTION_CONTAINER_NAME}"
