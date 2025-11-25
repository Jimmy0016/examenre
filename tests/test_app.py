import pytest
from app import app


@pytest.fixture
def client():
    # Configuramos la app en modo test
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_status_code(client):
    """Verifica que la ruta raíz devuelve código 200 OK."""
    response = client.get('/')
    assert response.status_code == 200


def test_hello_content(client):
    """Verifica que el HTML contiene el título esperado."""
    response = client.get('/')
    # Verificamos que 'Hola Mundo' esté en los datos de respuesta
    assert b"Hola Mundo" in response.data