from flask import Flask

app = Flask(__name__)


@app.route("/")  # E302: Se necesitan 2 líneas en blanco antes de definir la función
def hello():
    # HTML separado para cumplir con line-length y legibilidad
    html_content = (
        '<!DOCTYPE html>'
        '<html lang="es">'
        '<head>'
        '    <meta charset="UTF-8">'
        '    <title>Mi App Flask</title>'
        '    <style>'
        '        body { font-family: sans-serif; background-color: #f0f2f5; '
        '               display: flex; justify-content: center; '
        '               align-items: center; height: 100vh; margin: 0; }'
        '        .card { background: white; padding: 2rem; border-radius: 10px;'
        '                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); '
        '                text-align: center; }'
        '        h1 { color: #333; }'
        '    </style>'
        '</head>'
        '<body>'
        '    <div class="card">'
        '        <h1>🚀 Hola Mundo</h1>'
        '        <p>Probado con pytest y validado con flake8.</p>'
        '    </div>'
        '</body>'
        '</html>'
    )
    return html_content


if __name__ == "__main__":  # E305: Se necesitan 2 líneas en blanco antes de este bloque
    # E501: Rompemos los argumentos en varias líneas para no pasar 79 caracteres
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
# W292: Asegúrate de que haya una línea vacía aquí al final del archivo