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
    print(f"IP: {ip}")
    print(f"Cidade: {cidade}")
    print(f"Estado: {estado}")
    print(f"País: {pais}")
    print(f"ISP: {isp}")
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

    return """
<!DOCTYPE html>
<html>
<head>
<style>
body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:Arial;
}
</style>
</head>
<body>
    <h1>Site Online</h1>
</body>
</html>
"""


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
<!DOCTYPE html>
<html>
<head>
<style>
body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:Arial;
}

form{
    display:flex;
    flex-direction:column;
    gap:10px;
    width:250px;
}

input{
    padding:10px;
    text-align:center;
}

button{
    padding:10px;
    cursor:pointer;
}
</style>
</head>
<body>

<form method="post">
    <input name="senha" type="password">
</form>

</body>
</html>
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

    lista_visitas = ""

    for v in reversed(visitas):
        lista_visitas += f"""
        <tr>
            <td>{v['ip']}</td>
            <td>{v['cidade']}</td>
            <td>{v['estado']}</td>
            <td>{v['pais']}</td>
            <td>{v['isp']}</td>
        </tr>
        """

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
                height: 500px;
                width: 80%;
                margin: auto;
                border-radius: 10px;
            }}

            .panel {{
                width: 80%;
                margin: 20px auto;
                padding: 15px;
                background: #222;
                border-radius: 10px;
            }}

            button {{
                padding: 10px;
                margin: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                border: 1px solid #444;
                padding: 10px;
            }}

            th {{
                background: #333;
            }}
        </style>
    </head>

    <body>

    <h1>PAINEL ADMIN</h1>

    <div id="map"></div>

    <div class="panel">

    <h2>Visitas</h2>

    <table style="
        width:100%;
        border-collapse:collapse;
        text-align:center;
        ">

        <tr>
            <th>IP</th>
            <th>Cidade</th>
            <th>Estado</th>
            <th>País</th>
            <th>Operadora</th>
        </tr>

        {lista_visitas}

        </table>

        </div>

        <div class="panel">

<form method="POST" action="/admin/comando">

<input
    name="cmd"
    type="text"
    autocomplete="off"
    placeholder=">"
    style="
        width:100%;
        background:black;
        color:#00ff00;
        border:none;
        outline:none;
        font-family:Consolas, monospace;
        font-size:16px;
        padding:12px;
        box-sizing:border-box;
        border-radius:5px;
    "
>

</form>

</div>

    <script>

        var normal = L.tileLayer(
        'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
        {{
            attribution: 'OpenStreetMap'
        }}
        );

        var satelite = L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}',
        {{
            attribution: 'Esri'
        }}
        );

        var map = L.map('map', {{
            center: [0, 0],
            zoom: 2,
            layers: [satelite]
        }});

L.control.layers(
    {{
        "Mapa": normal,
        "Satélite": satelite
    }}
).addTo(map);

{markers}

</script>

    </body>
    </html>
    """
@app.route("/admin/comando", methods=["POST"])
def comando():

    if not session.get("logado"):
        return redirect("/admin/login")

    cmd = request.form.get("cmd", "").strip().lower()

    if cmd == "/sair":
        return redirect("/admin/logout")

    return redirect("/admin")

# -------------------
# LOGOUT
# -------------------
@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)