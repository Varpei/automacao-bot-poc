import urllib.request
import json
from config import load_env, required

load_env()

def testar_servico(nome, url, headers=None, method="GET", data=None):
    print(f"🔍 A testar {nome} ({url})...")
    try:
        req_data = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers or {}, method=method)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode()
            print(f"   [SUCESSO] {nome} respondeu com HTTP {response.status}")
            return True, body
    except Exception as e:
        print(f"   [FALHA] {nome} falhou: {e}")
        return False, str(e)

print("=== INÍCIO DA AUDITORIA GERAL DA APLICAÇÃO ===")

# 1. Testar Evolution API - Estado da Instância
ok_evo, _ = testar_servico(
    "Evolution API (instância configurada)",
    f"{required('EVOLUTION_SERVER_URL')}/instance/connectionState/{required('WHATSAPP_CLIENT_NAME')}",
    headers={"apikey": required("EVOLUTION_API_KEY")}
)

# 2. Testar Webhook configurado na Evolution API
ok_web, res_web = testar_servico(
    "Webhook na Evolution API",
    f"{required('EVOLUTION_SERVER_URL')}/webhook/find/{required('WHATSAPP_CLIENT_NAME')}",
    headers={"apikey": required("EVOLUTION_API_KEY")}
)
if ok_web and all(
    url not in res_web
    for url in (
        f"{required('N8N_WEBHOOK_URL').rstrip('/')}/webhook/{required('N8N_WEBHOOK_PATH')}",
        required("EVOLUTION_WEBHOOK_URL"),
    )
):
    print("   ⚠️ ATENÇÃO: A URL do Webhook configurada parece estar incorreta ou ausente!")

# 3. Testar n8n
testar_servico(
    "n8n (Health)",
    f"{required('N8N_WEBHOOK_URL').rstrip('/')}/"
)

# 4. Testar Ollama (IA Local)
testar_servico(
    "Ollama (Servidor Local)",
    required("OLLAMA_TAGS_URL")
)

print("=== FIM DA AUDITORIA GERAL ===")
