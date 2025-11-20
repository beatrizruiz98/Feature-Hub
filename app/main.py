"""Punto de entrada de la aplicación FastAPI: configura CORS, routers y metadatos de OpenAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings  # Mantiene la configuración disponible en todo el módulo.
from .database import engine
from .routers import auth, comments, features, likes

# Crear automáticamente las tablas definidas en models al iniciar la app (útil en desarrollo).
from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)

tags_metadata = [
    {"name": "Authentication", "description": "Registro, login y perfil del usuario autenticado."},
    {"name": "Features", "description": "CRUD de features, métricas de likes y comentarios asociados."},
    {"name": "Likes", "description": "Operaciones para votar o retirar votos sobre un feature."},
    {"name": "Comments", "description": "Gestión individual de comentarios creados por los usuarios."},
    {"name": "Health", "description": "Utilidades de supervisión para confirmar la disponibilidad del servicio."},
]

# Instancia principal de FastAPI exportada al servidor ASGI.
app = FastAPI(
    title="Feature Hub API",
    description="API construida con FastAPI y SQLModel para priorizar funcionalidades con likes y comentarios.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

# Fuentes permitidas para peticiones provenientes de navegadores.
origins = [
    "http://192.168.1.128",
    "http://localhost",
    "http://192.168.1.46"
]

# Middleware encargado de la negociación CORS (métodos, headers, cookies, etc.).
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro modular de cada conjunto de endpoints.
app.include_router(features.router)
app.include_router(auth.router)
app.include_router(likes.router)
app.include_router(comments.router)


@app.get(
    "/",
    summary="Ping",
    description="Endpoint de salud sencillo para comprobar que el servicio está vivo.",
    tags=["Health"],
)
def root():
    """Endpoint de salud sencillo para comprobar que el servicio está vivo."""
    return {"Server status": "Alive"}
