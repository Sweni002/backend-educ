# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier uniquement le fichier requirements.txt d'abord (optimisation du cache)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier app contenant ton code FastAPI
COPY ./app ./app

# Exposer le port 8000 (FastAPI par défaut)
EXPOSE 8000

# Commande pour lancer le serveur FastAPI avec rechargement automatique (--reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
