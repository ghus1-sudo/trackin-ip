from flask import Flask, request, session, redirect
import os
import requests
import bcrypt

app = Flask(__name__) 
app.secret_key = os.environ.get("SEcRET_KeY")
SENHA_HASH = os.environ.get("HAshPasS").encode()

visitas = []

# -------------------
# SITE NORMAL
# -------------------
@app.route("/")
def home():

    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

    cidade = estado = pais = isp = "Desconhecido"
    lat = lon = None

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()

        if data.get("status") == "success":
            cidade = data.get("city")
            estado = data.get("regionName")
            pais = data.get("country")
            isp = data.get("isp")
            lat = data.get("lat")
            lon = data.get("lon")

    except:
        pass
    print("===================================================")
    print(f"IP: {ip}<br>Cidade: {cidade}<br>Estado: {estado}<br>País: {pais}<br>ISP: {isp}")
    print("===================================================")

    visitas.append({
        "ip": ip,
        "cidade": cidade,
        "estado": estado,
        "pais": pais,
        "isp": isp,
        "lat": lat,
        "lon": lon
    })

    return "<h1 text-align: center;>Site Online</h1>"


# -------------------
# LOGIN
# -------------------
@app.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        senha = request.form.get("senha").encode()

        if bcrypt.checkpw(senha, SENHA_HASH):
            session["logado"] = True
            return redirect("/admin")
        else:
            return "Senha incorreta"

    return """
    <h1>Login Admin</h1>
    <form method="post">
        <input name="senha" type="password">
        <button>Entrar</button>
    </form>
    """


# -------------------
# ADMIN COM MAPA + COMANDOS
# -------------------
@app.route("/admin")
def admin():

    if not session.get("logado"):
        return redirect("/admin/login")

    markers = ""

    for v in visitas:
        if v["lat"] and v["lon"]:
            markers += f"""
            L.marker([{v['lat']}, {v['lon']}])
            .addTo(map)
            .bindPopup("{v['ip']}<br>{v['cidade']} - {v['estado']}<br>{v['pais']}<br>{v['isp']}");
            """

    comandos = "<br>".join([
        "TOTAL VISITAS: " + str(len(visitas)),
        "COMANDO: /clear (ainda não ativo)",
        "COMANDO: /stats (ainda não ativo)"
    ])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel</title>

        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

        <style>
            body {{
                font-family: Arial;
                text-align: center;
                background: #111;
                color: white;
            }}

            #map {{
                height: 350px;
                width: 80%;
                margin: auto;
                border-radius: 10px;
            }}

            .panel {{
                margin-top: 20px;
                padding: 15px;
                background: #222;
                width: 80%;
                margin-left: auto;
                margin-right: auto;
                border-radius: 10px;
                text-align: left;
            }}

            button {{
                padding: 10px;
                margin: 5px;
            }}
        </style>
    </head>

    <body>

    <h1>PAINEL ADMIN</h1>

    <div id="map"></div>

    <div class="panel">
        <h3>Comandos / Informações</h3>
        <p>{comandos}</p>

        <button onclick="alert('Comando futuro')">TESTE COMANDO</button>
        <button onclick="location.href='/admin/logout'">SAIR</button>
    </div>

    <script>
        var map = L.map('map').setView([0, 0], 2);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: 'OpenStreetMap'
        }}).addTo(map);

        {markers}
    </script>

    </body>
    </html>
    """


# -------------------
# LOGOUT
# -------------------
@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)