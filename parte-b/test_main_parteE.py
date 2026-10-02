from fastapi.testclient import TestClient
from main import app   # el FastAPI de su API

client = TestClient(app)

testLibreria = []
#E1 — Tu primer test de API

def test_get_libros_devuelve_lista():
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)

#E2 — Automatizá el 422 de B4

def test_agregar_libro():
    libro_nuevo = {
        "titulo": "cien años de soledad",
        "autor": "Gabriel Garcia Marquez",
        "paginas": 420,
        "disponible": True
    }
    posteo = client.post("/libros", json=libro_nuevo)
    testLibreria.append(posteo)
    assert posteo.status_code == 201  
    assert isinstance(posteo.json(), dict)

#E3 ambos caminos

def test_agregar_invalido():
    libro_invalido = {
        "titulo": "mil años de soledad",
        "autor": "dibu martinez",
        "paginas": 0,
        "disponible": True
    }
    posteo = client.post("/libros", json=libro_invalido)
    assert posteo.status_code == 422  
    assert isinstance(posteo.json(), dict)

def test_get_libros_devuelve_libro():
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
    
    titulos = [libro["titulo"] for libro in respuesta.json()]
    assert "cien años de soledad" in titulos