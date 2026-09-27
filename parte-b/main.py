# uvicorn main:app --reload
#venv\Scripts\activate.bat
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

libro1 ={
    "titulo": "cien años de soledad",
    "autor": "Gabriel Garcia Marquez",
    "paginas": 420,
    "disponible": True
}

libro2 ={
    "titulo": "rebelion en la granja",
    "autor": "George Orwell",
    "paginas": 190,
    "disponible": False
}


libro3 ={
    "titulo": "fahrenheit 451",
    "autor": "ray bradbury",
    "paginas": 172,
    "disponible": True,
    "editorial":{
        "nombre":"minotauro",
        "pais": "españa"
    }
}
libreria = []
libreria.append(libro1)
libreria.append(libro2)
libreria.append(libro3)

class Editorial(BaseModel): # dic anidado siempre primero, el 
    nombre: str             # principal ultimo.
    pais: str

class Libro(BaseModel): # para poder anidar dics, es recomendable que
    titulo: str         # cada dics tenga su propia clase. asi fastapi
    autor: str          # te tira un 422 si esta mal formado el body.
    paginas: int = Field(gt=0)
    disponible: bool = True
    editorial: Editorial | None = None
    costo_interno: float = 0.0     # siempre tiene que haver un valor default,  
#el apartado "Editorial | None = None"  # tal como "=none".
# se puede reemplazar por
#"editorial: Optional[Editorial] = None"

@app.get("/libros")  # b2 & b11 - listar con filtro opcional
def listar(paginas_min: int | None = None):
    if paginas_min is not None:
        return [libro for libro in libreria if libro["paginas"] >= paginas_min]
    return libreria

@app.get("/") #b1 - endpoint
def read_root():
    return {"mensaje": "Hola mundo"}

@app.get("/libros/{libro}") #b5 - get some/thing
def leer_libro(libro: str):
    for i in libreria:              
        if i["titulo"] == libro:   
            return libro                
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/libros/{libro}") # b6 - put/actualizar
def actualizar(libro: str, item: Libro):
    for i,book in enumerate(libreria):
        if book["titulo"] == libro:
            libreria[i] = item.model_dump()
            return libreria[i]
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/libros/{libro}", status_code=status.HTTP_204_NO_CONTENT) #b7 - delete some/thing
def borrar_campo(libro: str):
    for i,book in enumerate(libreria):              
        if book["titulo"] == libro:   
            libreria.pop(i)
            return                 
    raise HTTPException(status_code=404, detail="Libro no encontrado")
       
@app.post("/libros", response_model=Libro, status_code=status.HTTP_201_CREATED) #b3 - crear
def crear(item: Libro):
    libreria.append(item.model_dump())
    return item

#B4 - probando el error 422 me salieron
# que las 2 primeras eran errores de tipeo
# y la ultima directamente me tira json_error.

class Autor(BaseModel):
    nombre: str
    nacionalidad: str

autor1 = {"nombre": "Gabriel Garcia Marquez", "nacionalidad": "Colombia"}
autor2 = {"nombre": "George Orwell", "nacionalidad": "Reino Unido"}
autor3 = {"nombre": "Ray Bradbury", "nacionalidad": "Estados Unidos"}

autores = []
autores.append(autor1)
autores.append(autor2)
autores.append(autor3)


@app.get("/autores")  # b9 - listar autores
def listar_autores():
    return autores


@app.post("/autores", status_code=status.HTTP_201_CREATED)  # b9 - crear autor
def crear_autor(item: Autor):
    autores.append(item.model_dump())
    return item