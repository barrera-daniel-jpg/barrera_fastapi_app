# 1. Usar una imagen oficial de Python ligera
FROM python:3.12-slim

# 2. Evitar que Python genere archivos .pyc y forzar la salida en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app
# Instalar dependencias del sistema operativo (Compiladores)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# 4. Copiar solo el archivo de dependencias primero (optimiza el caché de Docker)
COPY requirements.txt .

# 5. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código del proyecto al contenedor
COPY . .

# 7. Exponer el puerto que usa FastAPI
EXPOSE 8000

# 8. Comando para ejecutar la aplicación (Asumiendo que tu archivo principal se llama main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]