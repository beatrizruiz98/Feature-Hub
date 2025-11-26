FROM python:3.14-slim

WORKDIR /usr/src/app 

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["fastapi", "run", "--host", "172.18.0.3", "--port", "5000"]

