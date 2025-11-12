from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hola Mundo"

if __name__ == "__main__":
    # Escucha en todas las interfaces (necesario para Docker)
    app.run(host="0.0.0.0", port=80)
