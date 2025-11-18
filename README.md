# Feature Hub Project

Plataforma para **proponer funcionalidades (“features”), debatirlas a través de comentarios y priorizarlas mediante likes**. Construida con **FastAPI**, **SQLModel**, **JWT**, **PostgreSQL** y **Alembic**.

---

## Quickstart

### Requisitos

- **Python 3.11+**
- **PostgreSQL** en ejecución (local o remoto)
- **git** instalado

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/<tu_usuario>/feature-hub-project.git
cd feature-hub-project

# Crear entorno virtual
python -m venv venv
# En Windows: venv\Scripts\activate
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Variables de entorno

Configura un archivo **.env** en la raíz del proyecto con los parámetros que espera `app/config.py`:

```env
database_hostname=hostname
database_port=5432
database_username=username
database_password=password
database_name=database_name
secret_key=secret_key
algorithm=algorithm
access_token_expire_minutes=minutes
```

### Migraciones y arranque

```bash
alembic upgrade head        # aplica la última migración
uvicorn app.main:app --reload
#o bien: fastapi dev app/main.py
```

Documentación API disponibles:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Estructura del proyecto

```
app/
  main.py             # Configura FastAPI y el middleware CORS
  routers/
    features.py       # CRUD de features y consulta de likes
    comments.py       # Gestión de comentarios en cada feature
    likes.py          # Alta/baja de likes (dir=1 o dir=0)
    auth.py           # Registro, login y perfil del usuario
  models.py           # Tablas SQLModel: Users, Features, Likes, Comments
  schemas.py          # Modelos Pydantic para requests/responses
  database.py         # Sesión y engine de SQLModel
  oauth2.py           # Helpers para JWT y dependencia `get_current_user`
  utils.py            # Hashing/verificación con Argon2 (pwdlib)
  config.py           # Carga de variables de entorno con pydantic-settings
alembic/
  env.py
  versions/           # Migraciones versionadas
requirements.txt
README.md
```

---

## Stack y decisiones técnicas

- **FastAPI + SQLModel:** CRUD tipado, validación automática y compatibilidad con SQLAlchemy.
- **PostgreSQL + Alembic:** persistencia relacional y migraciones reproducibles.
- **OAuth2 + JWT:** autenticación basada en `password grant`.
- **Argon2/pwdlib:** hashing seguro de contraseñas.
- **pydantic-settings:** centraliza la configuración desde `.env`.
- **CORS middleware:** permite probar desde hosts locales predefinidos.

---

## Endpoints principales

| Método | Ruta                | Descripción                                                   | Auth |
|:-----:|---------------------|---------------------------------------------------------------|:----:|
| **POST**   | `/auth/register`    | Registrar usuario nuevo                                      | ❌   |
| **POST**   | `/auth/login`       | Obtener token JWT (OAuth2PasswordRequestForm)                | ❌   |
| **GET**    | `/auth/me`          | Perfil del usuario autenticado                               | ✅   |
| **GET**    | `/features`         | Listar features (paginación, búsqueda y filtros por autor)   | ✅   |
| **GET**    | `/features/{id}`    | Obtener resumen de un feature con conteo de likes            | ✅   |
| **POST**   | `/features`         | Crear feature propio                                         | ✅   |
| **PUT**    | `/features/{id}`    | Actualizar un feature del usuario                            | ✅   |
| **DELETE** | `/features/{id}`    | Eliminar un feature propio                                   | ✅   |
| **GET** | `/features/{id}/comments`    | Obtener los comentarios de una feature                                   | ✅   |
| **POST**   | `/likes`            | Agregar (`dir=1`) o quitar (`dir=0`) un like sobre un feature| ✅   |
| **GET**    | `/comments/{id}`    | Consultar un comentario puntual                              | ✅   |
| **POST**   | `/comments`         | Publicar comentario asociado a un feature                    | ✅   |
| **DELETE** | `/comments/{id}`    | Eliminar comentario propio                                   | ✅   |

Todas las rutas autenticadas requieren la cabecera:

```
Authorization: Bearer <access_token>
```

---

## Migraciones Alembic

```bash
alembic upgrade head        # aplica migraciones pendientes
alembic revision -m "msg"   # crea una nueva migración
alembic downgrade -1        # revierte la última migración
```

> En entornos productivos utiliza siempre **Alembic** en lugar de `SQLModel.metadata.create_all()`.

---

## Troubleshooting

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error conectando a la DB | Variables `.env` erróneas o Postgres caído | Verifica credenciales y que el servicio acepte conexiones |
| `401 Unauthorized` | Token ausente o expirado | Repite el login y envía `Authorization: Bearer <token>` |
| `404 Feature … was not found` | ID inexistente o eliminado por otro usuario | Comprueba que el recurso esté creado antes de invocar el endpoint |
| Respuesta CORS bloqueada | Origen no contemplado en `origins` (app/main.py) | Añade el host al listado permitido |

---

## Licencia

**MIT © 2025 [Beatriz]**
