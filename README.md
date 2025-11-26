# Feature Hub Project

Featurehub es una aplicación basada en microservicios que expone una plataforma para **proponer funcionalidades (“features”), debatirlas a través de comentarios y priorizarlas mediante likes**. 

Incluye:

- API REST construida con **FastAPI**
- Base de datos **PostgreSQL** con migraciones **Alembic**
- Autenticación de usuarios basado en **OAuth2** y **JWT**.
- Frontend estático **HTML/JS/CSS**
- Reverse proxy **Nginx** para servir la app
- Todas los servicios están **dockerizados** 
- Despliegue completo mediante **Docker Compose**

---

## 🏗️ Arquitectura

![alt text](arq.png)

## Quickstart

### 🚀 Tecnologías

- FastAPI + SQLModel
- PostgreSQL
- Alembic (migraciones)
- Argon2 (hashing)
- OAuth2 + JWT
- Docker & Docker Compose
- Nginx

### Requisitos

- **Docker**

### Despliegue

#### 1. Clonar el repositorio
```bash
git clone https://github.com/beatrizruiz98/Feature-Hub
cd Feature-Hub
```

#### 2. Crear archivo .env

Configura un archivo **.env** en la raíz del proyecto con los parámetros que espera la aplicación:

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

#### 3. Levantar la app

- Desarrollo 
```bash
docker compose -f docker-compose-dev.yml up --build
```
- Entorno productivo
```bash
docker compose -f docker-compose-prod.yml up
```
*Cuando se realicen cambios en las imagenes y se precise disponerlas en el entorno productivo se deberán etiquetar y subir a dockerhub.*

### Migraciones
```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic revision -m "change"
docker compose exec api alembic downgrade -1
```
---

## Estructura del proyecto

```
backend/  
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
  Dockerfile            # Instrucciones para crear imagen api
nginx/ 
  /front                # HTML, JS, CSS
    index.html
    /static
      app.js
      styles.css
  featurehub.conf       # Configuración del servidor que sirve la app
  nginx.conf            # Congiguración nginx
docker-compose-dev.yml  # Despliegue en dev (servicios basados en build, comando fastapi dev, volumen para desarrollo)
docker-compose-prod.yml # Despliegue production (servicios basados en image, sin volumen para desarrollo)     
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
- **Nginx** sirve la aplicación a través de un proxy inverso. Garantiza alto rendimiento y eficiencia. Fácil configuración.

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
*En el frontend no están disponibles las funcionalidades PUT /features, DELETE /features, DELETE /comments*

---

## Troubleshooting

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error conectando a la DB | Variables `.env` erróneas o Postgres caído | Verifica credenciales y que el servicio acepte conexiones |
| `401 Unauthorized` | Token ausente o expirado | Repite el login y envía `Authorization: Bearer <token>` |
| `404 Feature … was not found` | ID inexistente o eliminado por otro usuario | Comprueba que el recurso esté creado antes de invocar el endpoint |
| Respuesta CORS bloqueada | Origen no contemplado en `origins` (app/main.py) | Añade el host al listado permitido |
| Error de networking entre frontend y backend | Direcciones erróneas en featurehub.conf, Dockerfile (api) | Revisar redes `docker network inspect <red_docker>`, revisar peticiones entre servicios `tshark -i <interfaz_servicio> -f "tcp port <puerto_servicio>" -Y "http"`|

---

## Licencia

**MIT © 2025 [Beatriz]**


