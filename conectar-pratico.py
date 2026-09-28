import urllib.request
import json
import base64
import os
from config import load_env, required

load_env()

# Configurações da requisição
url = f"{required('EVOLUTION_SERVER_URL')}/instance/connect/{required('WHATSAPP_CLIENT_NAME')}"
headers = {"apikey": required("EVOLUTION_API_KEY")}
req = urllib.request.Request(url, headers=headers)

print("Solicitando novo QR Code para a Evolution API...")

try:
    # Faz a chamada HTTP e lê a resposta
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        base64_str = data.get("base64", "")
        
        # Verifica se o retorno contém a string de imagem
        if base64_str.startswith("data:image/png;base64,"):
            # Remove o cabeçalho do base64 para ficar só com os dados binários
            base64_data = base64_str.split(",")[1]
            
            # Decodifica e salva fisicamente o arquivo PNG
            with open("qrcode.png", "wb") as f:
                f.write(base64.b64decode(base64_data))
            
            print("✅ Sucesso! O arquivo 'qrcode.png' foi salvo na raiz do seu projeto.")
            print("👉 Clique nele no VS Code para visualizar e escanear com seu WhatsApp.")
        else:
            print("⚠️ Não foi possível obter o QR Code. A instância já pode estar conectada.")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
