from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def inicio():
    ip = request.remote_addr

    print(f"IP detectado: {ip}")

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Meu Site</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                margin-top: 100px;
            }

            h1 {
                color: blue;
            }
        </style>
    </head>
    <body>
        <h1>Olá!</h1>
        <p>Você acessou meu site.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
