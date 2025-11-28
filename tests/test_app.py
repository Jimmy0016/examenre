import pytest
from app import app

@pytest.fixture
def client():
    # Prepara la aplicación para pruebas
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """Verifica que la página carga (código 200)"""
    response = client.get('/')
    assert response.status_code == 200

def test_home_content(client):
    """Verifica que aparece el texto correcto"""
    response = client.get('/')
    # Buscamos la palabra clave en el HTML devuelto
    assert b"EXAMENES" in response.data