FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Installer TA-Lib
RUN curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz | tar xz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY bot/ ./bot/
COPY bot_config.yaml .

# Créer les dossiers nécessaires
RUN mkdir -p logs data

# Exposer les ports
EXPOSE 8000 9090

# Variables d'environnement
ENV PYTHONPATH=/app
ENV CONFIG_PATH=/app/bot_config.yaml

# Commande par défaut
CMD ["python", "-m", "bot.apps.main"]
