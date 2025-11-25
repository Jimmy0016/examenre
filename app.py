from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    # Usamos HTML y CSS en línea para una presentación más atractiva
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Mi App Flask</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 { color: #333; }
            p { color: #666; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Hola Mundo</h1>
            <p>Ejecutándose desde Flask con estilo.</p>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    # Puerto 5000 es el estándar para desarrollo (el 80 suele requerir permisos de root)
    app.run(host="0.0.0.0", port=5000, debug=True)