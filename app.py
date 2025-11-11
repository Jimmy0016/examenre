from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "👋 Hola Mundo desde Flask y CI/CD con GitHub Actions 🚀"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
