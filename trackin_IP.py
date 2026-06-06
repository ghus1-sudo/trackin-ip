from flask import Flask, request
import requests

app = Flask(__name__)

visitas = []

ADMIN_PASSWORD = "1234"  # 🔐 MUDA ISSO DEPOIS

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

    # 🔥 LOG COMPLETO NO RENDER
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


# 🔐 LOGIN SIMPLES ADMIN
@app.route("/admin")
def admin():

    senha = request.args.get("senha")

    if senha != ADMIN_PASSWORD:
        return """
        <h1>Acesso negado</h1>
        <p>Use /admin?senha=1234</p>
        """

    return """
    <h1>Carregando mapa...</h1>
    <script>
        setTimeout(() => {
            location.reload();
        }, 5000);
    </script>
    """ + gerar_mapa()


def gerar_mapa():

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
        <title>Admin Map</title>

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

    <h1>Mapa em Tempo Real</h1>
    <p>Total de visitas: {len(visitas)}</p>

    <div id="map"></div>

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)