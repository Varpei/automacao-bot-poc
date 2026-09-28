import urllib.request
import json
import os
from config import load_env, required

load_env()

url = f"{required('EVOLUTION_SERVER_URL')}/instance/connectionState/{required('WHATSAPP_CLIENT_NAME')}"
headers = {"apikey": required("EVOLUTION_API_KEY")}
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("🔍 Estado da Conexão:", json.dumps(data, indent=2))
except Exception as e:
    print(f"❌ Erro ao consultar a Evolution API: {e}")
