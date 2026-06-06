from flask import Flask, request, session, redirect
import os
import requests
import bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get("SEcRET_KeY")

# 🔐 COLE AQUI O HASH GERADO
SENHA_HASH = os.environ.get("HAshPasS").encode()

visitas = []

# --------------------
# SITE NORMAL
# --------------------
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

    # 🔥 LOG NO RENDER (:contentReference[oaicite:0]{index=0})
    print("====================================")
    print(f"IP: {ip}")
    print(f"Cidade: {cidade}")
    print(f"Estado: {estado}")
    print(f"País: {pais}")
    print(f"Operadora: {isp}")
    print("====================================")

    visitas.append({
        "ip": ip,
        "cidade": cidade,
        "estado": estado,
        "pais": pais,
        "isp": isp,
        "lat": lat,
        "lon": lon
    })

    return "<h1>Site Online</h1>"


# --------------------
# LOGIN ADMIN
# --------------------
@app.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        senha = request.form.get("senha").encode()

        if bcrypt.checkpw(senha, SENHA_HASH):
            session["logado"] = True
            return redirect("/admin")
        else:
            return "<h1>Senha incorreta</h1>"

    return """
    <h1>Login Admin</h1>
    <form method="post">
        <input type="password" name="senha" placeholder="Senha">
        <button type="submit">Entrar</button>
    </form>
    """


# --------------------
# ADMIN (MAPA)
# --------------------
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

    return f"""
    <html>
    <head>
        <title>Admin</title>

        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

        <style>
            body {{
                font-family: Arial;
                text-align: center;
            }}
            #map {{
                height: 600px;
                width: 90%;
                margin: auto;
            }}
        </style>
    </head>

    <body>

    <h1>Painel Seguro</h1>
    <p>Total de visitas: {len(visitas)}</p>

    <a href="/admin/logout">Sair</a>

    <div id="map"></div>

    <script>
        var map = L.map('map').setView([0, 0], 2);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

        {markers}
    </script>

    </body>
    </html>
    """


# --------------------
# LOGOUT
# --------------------
@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)