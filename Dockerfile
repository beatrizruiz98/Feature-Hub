FROM python:3.9.7

WORKDIR /usr/src/app # Set Directorio de trabajo en el contenedor (donde lanzo los comandos)

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . # Copio todo el codigo fuente en el directorio (. = /usr/src/app)

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "80000"]

