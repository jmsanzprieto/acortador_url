import json
import os
import string
import random

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
URLS_FILE = os.getenv("URLS_FILE", "urls.json")

# Cargar plantilla
templates = Jinja2Templates(directory="templates")
app = FastAPI()


# Leer JSON
def read_urls():
    """Reads the list of URL mappings from the JSON file."""
    if not os.path.exists(URLS_FILE):
        return [] # Retorna una lista vacía si el archivo no existe
    try:
        with open(URLS_FILE, "r") as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error leyendo {URLS_FILE}.")
        return []
    except Exception as e:
        print(f"Ocurrió un error leyendo {URLS_FILE}: {e}")
        return []


# Escribir JSON - Ahora escribe una lista
def guardar_urls(urls_list):
    """Writes the list of URL mappings to the JSON file."""
    try:
        with open(URLS_FILE, "w") as f:
            json.dump(urls_list, f, indent=4) # Usar indent para legibilidad
    except Exception as e:
        print(f"An error occurred while writing to {URLS_FILE}: {e}")

# --- Funciones auxiliares (sin cambios) ---

# Generar código corto
def generate_code(length=6):
    """Generates a random short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# --- Rutas de la aplicación (Modificaciones en /shorten y /{code}) ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten", response_class=HTMLResponse)
async def shorten_url(request: Request, url: str = Form(...)):
    """Acorta la URL y la guarda en un json."""
    urls_list = read_urls()

    # Verificar si ya existe (recorriendo la lista)
    for item in urls_list:
        # El código es la clave que no es "fecha_creacion"
        code_keys = [k for k in item.keys() if k != "fecha_creacion"]
        if code_keys and item[code_keys[0]] == url:
            existing_code = code_keys[0]
            short_url = f"{BASE_URL}/{existing_code}"
            return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url, "original_url": url})

    # Generar un nuevo código único
    code = generate_code()
    # Asegurarse de que el código no exista en la lista actual
    existing_codes = {code_keys[0] for item in urls_list for code_keys in [[k for k in item.keys() if k != "fecha_creacion"]] if code_keys}
    while code in existing_codes:
         code = generate_code()

    # Crear el nuevo item en el formato deseado
    new_item = {
        "fecha_creacion": datetime.now().isoformat(), # ISO format para la fecha
        code: url
    }

    # Añadir el nuevo item a la lista y guardar
    urls_list.append(new_item)
    guardar_urls(urls_list)

    short_url = f"{BASE_URL}/{code}"
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url, "original_url": url})

@app.get("/{code}")
async def redirect(code: str):
    """Redirige a la url original."""
    urls_list = read_urls()

    # Buscar el código en la lista de items
    for item in urls_list:
        # El código es la clave que no es "fecha_creacion"
        code_keys = [k for k in item.keys() if k != "fecha_creacion"]
        if code_keys and code_keys[0] == code:
            original_url = item[code_keys[0]]
            return RedirectResponse(original_url)

    # Si el código no se encuentra
    return HTMLResponse(content="URL no encontrada", status_code=404)

# Opcional: Añadir un endpoint para ver los datos crudos (para depuración)
@app.get("/data/raw")
async def get_raw_data():
    """
    Devuelve el contenido bruto del archivo urls.json (para analizar).
    """

    try:
        with open(URLS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "urls.json no encontrado"}, 404
    except json.JSONDecodeError:
        return {"error": "No puedo decodificar urls.json"}, 500