from flask import Flask
from app.services.connect_db import db

# Initialisation de l'application Flask
app = Flask(__name__)

# Vérifier la connexion à la base donnée
try:
    # Vérifier que la connexion à mongoDB est active
    db.client.admin.command('ping') # Ping pour s'assurer que la connexion est reussie
    print("--------------------")
    print("Connexion MongoDB établie !!!")
    print("--------------------")
except Exception as error :
    # En cas d'erreur de connexion, affiche un message d'erreur
    print(f"Erreur de connexion à mongoDB : \n {error}")

# Importer les routes après l'initialisation
from app.routes import task