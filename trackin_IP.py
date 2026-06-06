from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():

    # pega IP real (Render usa proxy)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

    cidade = "Desconhecida"
    pais = "Desconhecido"

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()

        if data.get("status") == "success":
            cidade = data.get("city", "Desconhecida")
            pais = data.get("country", "Desconhecido")

    except:
        pass

    # 🔥 SÓ LOG (NÃO aparece no site)
    print("===================================")
    print(f"IP: {ip}")
    print(f"Cidade: {cidade}")
    print(f"País: {pais}")
    print("===================================")

    return """
    <h1>Site Online</h1>
    <p>Bem-vindo!</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)