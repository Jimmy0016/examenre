Proyecto Taller: Pipeline CI/CD (de Push a Paquete)

Este repositorio es un ejemplo práctico de un pipeline de Integración Continua (CI) y Entrega Continua (CD) utilizando GitHub Actions, Python (Flask), Pytest, y Docker.

El objetivo es automatizar el proceso desde que un desarrollador sube un cambio (push) hasta que se genera un artefacto listo para desplegar (un "Package", en este caso, una imagen de Docker).

 Estructura del Repositorio
```
.
├── .github/workflows/
│   └── ci.yml             # ⬅️ Define todo el pipeline de CI/CD
├── tests/
│   └── test_app.py        # ⬅️ Pruebas unitarias para la aplicación
├── app.py                 # ⬅️ Aplicación web simple (Flask)
├── Dockerfile             # ⬅️ Instrucciones para construir la imagen Docker (el paquete)
├── Makefile               # (Opcional) Atajos para construir y desplegar
├── README.md              # (Este archivo)
├── requirements.txt       # ⬅️ Dependencias de Python
└── stack.yml              # (Opcional) Archivo de despliegue para Docker Swarm
``` 

¿Qué es CI/CD?

Integración Continua (CI): Es la práctica de fusionar automáticamente los cambios de código de todos los desarrolladores en un repositorio central varias veces al día. Cada integración se verifica mediante una compilación y pruebas automatizadas.

Entrega/Despliegue Continuo (CD): Es el paso siguiente.

Entrega Continua: Lleva el código validado por la CI y lo "empaqueta" (ej. una imagen Docker), dejándolo listo y almacenado en un "artifact repository" (como GHCR) para que pueda ser desplegado manualmente.

Despliegue Continuo: Va un paso más allá y despliega automáticamente ese paquete en producción.

Este ejemplo se centra en el CI y la parte de "Entrega Continua" (construcción del paquete).

Análisis Detallado del Pipeline (ci.yml)

Nuestro pipeline se define en .github/workflows/ci.yml. Vamos a analizarlo paso a paso.

name: "CI/CD Pipeline"

on:
  push:
    branches:
      - Jordy
  pull_request:


name: El nombre del flujo de trabajo que aparecerá en la pestaña "Actions" de GitHub.

on: Define los disparadores (triggers). Este pipeline se ejecutará automáticamente cada vez que alguien haga un push a la rama Jordy o cuando se cree un pull_request.

Fase 1: El Trabajo de build (CI)

El pipeline tiene un solo "trabajo" (job) llamado build que se ejecuta en una máquina virtual de Ubuntu.

jobs:
  build:
    runs-on: ubuntu-latest


Estos son los pasos que realiza:

Paso 1: Descargar el Código

    # ✅ Descargar el código del repositorio
    - name: "Checkout repository"
      uses: actions/checkout@v3


Este paso utiliza una "Action" predefinida por GitHub (actions/checkout) para descargar el código fuente de tu repositorio en la máquina virtual.

Paso 2: Configurar el Entorno

    # ✅ Configurar Python 3.10
    - name: "Set up Python"
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    # ✅ Instalar dependencias
    - name: "Install dependencies"
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt


Aquí preparamos el entorno. Primero, instalamos la versión de Python 3.10. Luego, usamos pip para instalar todas las bibliotecas listadas en requirements.txt (flask, pytest, flake8).

Paso 3: Pruebas y Calidad de Código (El Corazón de la CI)

Este es el paso más crítico de la Integración Continua. Si falla, el pipeline se detiene y el desarrollador es notificado.

    # ✅ Linter para calidad de código
    - name: "Run lint"
      run: flake8 .


Prueba Estática (Linting): flake8 . revisa todo tu código Python sin ejecutarlo. Busca errores de sintaxis, código que no sigue las guías de estilo (PEP 8), variables no usadas, etc. Es una primera barrera de calidad.

    # ✅ Ejecutar pruebas
    - name: Run tests
      run: |
        export PYTHONPATH=$PYTHONPATH:$(pwd)
        pytest tests


Prueba Dinámica (Unit Testing): pytest tests ejecuta las pruebas definidas en la carpeta tests/. En nuestro caso, ejecuta tests/test_app.py.

Ejemplo de Prueba (tests/test_app.py)

Esta prueba verifica que nuestra aplicación app.py funcione como se espera.

# Contenido de tests/test_app.py
from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hola Mundo" in response.data


Esta prueba:

Importa la app de Flask.

Crea un cliente de prueba.

Simula una petición GET a la ruta raíz (/).

assert response.status_code == 200: Verifica que la página devuelva un código "OK".

assert b"Hola Mundo" in response.data: Verifica que el contenido de la página sea el esperado.

Si cualquiera de estas afirmaciones (assert) falla, pytest fallará, y por lo tanto, el pipeline de CI fallará.

Fase 2: Construcción del Paquete (CD)

¡Felicidades! Si el pipeline llega hasta aquí, significa que el código es correcto, sigue los estándares de calidad y pasa todas las pruebas.

Ahora comienza la fase de Entrega Continua (CD): construir nuestro artefacto o "paquete".

Paso 4: Iniciar Sesión en el Registro de Paquetes

    # ✅ Login en GitHub Container Registry
    - name: "Login to GHCR"
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}


ghcr.io: Es el registro de contenedores de GitHub (GitHub Container Registry). Es donde almacenaremos nuestra imagen de Docker.

docker/login-action: Es una "Action" que nos permite autenticarnos en un registro de Docker.

secrets.GITHUB_TOKEN: Es un token temporal que GitHub crea automáticamente para cada ejecución del pipeline, dándole permiso para escribir en el registro de paquetes de este repositorio.

Paso 5: Construir y Subir el "PACKAGE"

Este es el paso final de nuestro proceso: la construcción y publicación del paquete.

    # ✅ Construir y subir la imagen Docker
    - name: "Build and push Docker image"
      uses: docker/build-push-action@v4
      with:
        push: true
        tags: ghcr.io/jordysz/jordy_sanchez_taller:latest


docker/build-push-action: Esta Action orquesta todo el proceso de docker build y docker push.

push: true: Le indica a la acción que, después de construir la imagen, debe subirla (push) al registro en el que iniciamos sesión.

tags: Es el nombre completo de nuestra imagen (nuestro paquete).

ghcr.io: El registro.

jordysz: El nombre de usuario o propietario.

jordy_sanchez_taller: El nombre de la imagen (paquete).

:latest: La etiqueta (versión) de la imagen.

La Receta del Paquete (Dockerfile)

La acción anterior (docker/build-push-action) no sabría qué hacer sin nuestro Dockerfile, que actúa como la receta para construir la imagen:

# Contenido del Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]


Esta receta le dice a Docker:

Empieza con una imagen base ligera de Python 3.10.

Crea un directorio /app y establécete allí.

Copia todos los archivos del repositorio (como app.py, requirements.txt) dentro de /app.

Ejecuta pip install dentro de la imagen para instalar las dependencias.

Define el comando por defecto para ejecutar cuando se inicie el contenedor: python app.py.

Conclusión del Ciclo

Al final de este pipeline:

(CI) Hemos verificado que el código nuevo es de alta calidad y no rompe ninguna funcionalidad existente.

(CD) Hemos creado un paquete (la imagen Docker ghcr.io/jordysz/jordy_sanchez_taller:latest) que contiene nuestra aplicación y todas sus dependencias, listo para ser ejecutado en cualquier lugar.

Este paquete está ahora almacenado en el GitHub Container Registry, completando el ciclo "de Push a Paquete".

Pasos Siguientes (Despliegue Continuo)

Los archivos Makefile y stack.yml que tienes sugieren el siguiente paso lógico: el Despliegue Continuo.

Un pipeline más avanzado podría añadir un segundo job que, al terminarse el build con éxito, se conecte a un servidor (vía SSH) y ejecute make deploy. Este comando usaría el stack.yml para decirle a Docker Swarm: "Oye, hay una nueva versión :latest de la imagen, descárgala y actualiza el servicio".