# Acortador de URL con FastAPI

Este proyecto es un sencillo acortador de URLs usando **FastAPI**. Permite a los usuarios introducir una URL larga a través de un formulario HTML, y devuelve una URL acortada que redirige a la original.

---

## Características
- Interfaz HTML para introducir URLs.
- Generación de códigos únicos para URLs acortadas.
- Redirección automática a la URL original al visitar la versión corta.
- Almacenamiento de las URLs en un archivo JSON.
- Configuración de la URL base desde un archivo `.env`.

---

## Estructura del proyecto

```
acortador_url/
├── main.py
├── urls.json
├── .env
├── requirements.txt
└── templates/
    └── index.html
```

---

## Requisitos

Instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

---

## Archivo `.env`

Debes crear un archivo `.env` en el directorio raíz con el siguiente contenido:

```
BASE_URL=http://localhost:8000
URLS_FILE=urls.json
```

---

## Uso

Ejecutar el servidor:
```bash
uvicorn main:app --reload
```

Accede en el navegador a: [http://localhost:8000](http://localhost:8000)

1. Introduce una URL en el formulario y haz clic en acortar.
2. Obtendrás una URL como `http://localhost:8000/abc123`.
3. Visítala y serás redirigido a la URL original.

---

## Dependencias

Incluidas en `requirements.txt`:
```
fastapi
uvicorn
python-dotenv
jinja2
python-multipart
```

---

## Autor
José Manuel Sanz - contacto@josemanuelsanz.es
Desarrollado como ejemplo educativo para construir una aplicación estilo Bit.ly con FastAPI.

