import requests

URL = "http://127.0.0.1:8000/libros"
session = requests.Session()

def get_libros():
    response = session.get(URL, timeout=5)
    return response

def crear_libro(payload):
    response = session.post(URL, json=payload, timeout=5)
    return response

def actualizar_libro(id_libro, payload):
    response = session.put(f"{URL}/{id_libro}", json=payload, timeout=5)
    return response

def borrar_libro(id_libro):
    response = session.delete(f"{URL}/{id_libro}", timeout=5)
    return response


# --- Pruebas ---

response = get_libros()
print("GET:", response.status_code, response.json())

nuevo_libro = {
    "titulo": "Frankenstein",
    "autor": "Mary Shelley",
    "paginas": 288,
    "disponible": False
}
response = crear_libro(nuevo_libro)
print("POST:", response.status_code, response.json())

libro_actualizado = {
    "titulo": "Frankenstein (edición revisada)",
    "autor": "Mary Shelley",
    "paginas": 300,
    "disponible": True
}
response = actualizar_libro(1, libro_actualizado)
print("PUT:", response.status_code, response.json())

response = borrar_libro(1)
print("DELETE:", response.status_code)

session.close()