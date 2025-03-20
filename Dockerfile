# Derleme aşaması
FROM python:3.11 AS builder

WORKDIR /app

# Derleme için gerekli paketleri yükle
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Sanal ortam oluştur
RUN python -m venv /opt/venv
# Sanal ortamı etkinleştir
ENV PATH="/opt/venv/bin:$PATH"

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Çalışma aşaması
FROM python:3.11-slim-buster

WORKDIR /app

# Derleme aşamasından sanal ortamı kopyala
COPY --from=builder /opt/venv /opt/venv

# Sanal ortamı etkinleştir
ENV PATH="/opt/venv/bin:$PATH"

# Uygulama dosyalarını kopyala
COPY app.py .
COPY templates templates
COPY static static

# Portu aç
EXPOSE 5000

# Uygulamayı başlat
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]