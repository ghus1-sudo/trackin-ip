from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def inicio():

    # pega IP real do visitante (funciona melhor no Render)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # API de localização pelo IP
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        cidade = data.get("city", "Desconhecida")
        pais = data.get("country", "Desconhecido")
        isp = data.get("isp", "Desconhecido")

    except:
        cidade = pais = isp = "Erro ao obter"

    print(f"IP: {ip} | {cidade}, {pais}")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Meu Site</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                margin-top: 100px;
            }}
            h1 {{
                color: blue;
            }}
        </style>
    </head>
    <body>
        <h1>Olá!</h1>
        <p>Seu IP: {ip}</p>
        <p>Cidade: {cidade}</p>
        <p>País: {pais}</p>
        <p>Provedor: {isp}</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)