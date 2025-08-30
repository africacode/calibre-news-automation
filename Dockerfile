FROM python:3.11-slim

# 👇 Esto te permite forzar un rebuild cuando quieras
ARG CACHE_BUST=1
ENV CACHE_BUST=${CACHE_BUST}

# Variables para evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PATH="/root/.local/bin:$PATH"

# Instalar dependencias necesarias y Calibre
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget curl xz-utils \
        libegl1 libopengl0 libxcb-cursor0 libxrender1 libxi6 libxcomposite1 libxrandr2 \
        libxdamage1 libxfixes3 libxkbcommon0 libxkbcommon-x11-0 libglib2.0-0 libfreetype6 \
        libfontconfig1 libharfbuzz0b libfribidi0 libjpeg62-turbo libnss3 libnspr4 \
        libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libasound2 libpng16-16 libx11-6 \
        libxext6 libxau6 libxdmcp6 zlib1g libbz2-1.0 libexpat1 libuuid1 libgl1 \
    && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin \
    && apt-get purge -y wget curl xz-utils \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copiar solo requirements primero para aprovechar caché
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear carpeta de salida
RUN mkdir -p /app/output

CMD ["python", "descargar_y_enviar.py"]

