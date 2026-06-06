from flask import Flask, request
import requests

app = Flask(__name__)

# "banco" simples em memória (só enquanto o servidor roda)
visitas = []

@app.route("/")
def inicio():

    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()

        cidade = data.get("city", "Desconhecida")
        pais = data.get("country", "Desconhecido")

    except:
        cidade = "Erro"
        pais = "Erro"

    # salva visita
    visitas.append({
        "ip": ip,
        "cidade": cidade,
        "pais": pais
    })

    print(f"{ip} - {cidade} - {pais}")

    # site normal pro usuário
    return """
    <h1>Site Online</h1>
    <p>Bem-vindo!</p>
    """


# 🔒 PAINEL SECRETO (só você)
@app.route("/admin")
def admin():

    html = "<h1>Mapa de visitantes</h1><ul>"

    for v in visitas:
        html += f"<li>{v['ip']} - {v['cidade']} - {v['pais']}</li>"

    html += "</ul>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)