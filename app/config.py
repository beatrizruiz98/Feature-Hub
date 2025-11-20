from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Agrupa toda la configuración sensible de la API cargada desde variables de entorno."""

    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # Indica a Pydantic qué archivo revisar si las variables no vienen del entorno.
        env_file = ".env"  # Le indico de donde coger las variables


# Instancia única que se importará desde cualquier módulo que necesite configuración.
settings = Settings()
