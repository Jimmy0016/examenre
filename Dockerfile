FROM python:3.10-slim

#  ESTA LÍNEA ES LA "MAGIA" QUE LO VINCULA A TU REPOSITORIO 👇
LABEL org.opencontainers.image.source=https://github.com/Jimmy0016/recuperacion.git

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]