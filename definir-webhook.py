import urllib.request
import urllib.error
import json
from config import load_env, required

load_env()

url = f"{required('EVOLUTION_SERVER_URL')}/webhook/set/{required('WHATSAPP_CLIENT_NAME')}"
headers = {
    "Content-Type": "application/json",
    "apikey": required("EVOLUTION_API_KEY")
}

# Payload rigorosamente estruturado com a chave 'webhook' na raiz
payload = {
    "webhook": {
        "enabled": True,
        "url": required("EVOLUTION_WEBHOOK_URL"),
        "webhookByEvents": False,
        "events": [
            "MESSAGES_UPSERT",
            "CONNECTION_UPDATE"
        ]
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("✅ Webhook configurado com sucesso:", json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    print(f"❌ A Evolution API rejeitou com HTTP {e.code}: {error_body}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
