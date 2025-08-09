FROM python:3.11-slim

# Instalar Calibre y dependencias
RUN apt-get update && apt-get install -y \
    calibre \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxkbcommon0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar todos los archivos del repositorio
COPY . .

# Instalar dependencias de Python si hay requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true

# Comando por defecto
CMD ["python3", "descargar_y_enviar.py"]
