from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def inicio():

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        cidade = data.get("city", "Desconhecida")
        pais = data.get("country", "Desconhecido")
        isp = data.get("isp", "Desconhecido")

    except:
        cidade = pais = isp = "Erro"

    # 🔥 SÓ NO LOG (NÃO aparece no site)
    print("====================================")
    print(f"IP: {ip}")
    print(f"Cidade: {cidade}")
    print(f"País: {pais}")
    print(f"ISP: {isp}")
    print("====================================")

    return """
    <h1>Site online</h1>
    <p>Bem-vindo!</p>
    """
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)