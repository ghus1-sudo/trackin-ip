from flask import Flask, request
import requests

app = Flask(__name__)

# guarda visitas (enquanto o servidor estiver ligado)
visitas = []

@app.route("/")
def home():

    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()

        cidade = data.get("city", "Desconhecida")
        pais = data.get("country", "Desconhecido")
        lat = data.get("lat")
        lon = data.get("lon")

    except:
        cidade = pais = "Erro"
        lat = lon = None

    print(f"VISITA: {ip} | {cidade} | {pais}")

    visitas.append({
        "ip": ip,
        "cidade": cidade,
        "pais": pais,
        "lat": lat,
        "lon": lon
    })

    return """
    <h1>Site Online</h1>
    <p>Bem-vindo!</p>
    """


@app.route("/admin")
def admin():

    markers = ""

    for v in visitas:
        if v["lat"] and v["lon"]:
            markers += f"""
            L.marker([{v['lat']}, {v['lon']}])
            .addTo(map)
            .bindPopup("{v['ip']}<br>{v['cidade']} - {v['pais']}");
            """

    return f"""
    <!DOCTYPE html>
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
                height: 500px;
                width: 90%;
                margin: auto;
            }}
        </style>
    </head>

    <body>

    <h1>Painel de Visitas</h1>
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