FROM python:3.11-slim

WORKDIR /app

# ✅ Systémové knihovny nutné pro prohlížeče Playwrightu
RUN apt-get update && apt-get install -y \
    wget gnupg libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libasound2 libpangocairo-1.0-0 libcairo2 libpango-1.0-0 \
    libx11-xcb1 libxext6 libxfixes3 libxshmfence1 xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Instalace Playwright + všech prohlížečů
RUN playwright install --with-deps chromium
RUN playwright install --with-deps firefox
RUN playwright install --with-deps webkit

# ✅ Zbytek aplikace
COPY . .

EXPOSE 8000

# ✅ Spuštění aplikace
CMD ["python", "app.py"]