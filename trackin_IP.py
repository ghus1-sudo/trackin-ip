from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def inicio():

    # pega só o IP real (remove proxies do Render)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

    try:
        # API de localização
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()

        # valida resposta da API
        if data.get("status") != "success":
            cidade = "Desconhecida"
            pais = "Desconhecido"
            isp = "Desconhecido"
        else:
            cidade = data.get("city", "Desconhecida")
            pais = data.get("country", "Desconhecido")
            isp = data.get("isp", "Desconhecido")

    except:
        cidade = "Erro"
        pais = "Erro"
        isp = "Erro"

    # 🔥 SÓ LOG (não aparece no site)
    print("====================================")
    print(f"IP: {ip}")
    print(f"Cidade: {cidade}")
    print(f"País: {pais}")
    print(f"ISP: {isp}")
    print("====================================")

    # site simples
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Site Online</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                margin-top: 100px;
            }
            h1 {
                color: green;
            }
        </style>
    </head>
    <body>
        <h1>Site Online</h1>
        <p>Bem-vindo ao meu site!</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)