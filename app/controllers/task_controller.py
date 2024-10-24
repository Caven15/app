from flask import  request, jsonify
from app.models.task_schema import TaskSchema
from app.services.connect_db import db

# définir la logique pour la communication avec la base de donnée 

# CRUD

# GetAll : Récupérer toute les tâches

# Create : Ajouter une tâche
def ajouter_tache():
    
    # Valider les données reçues à l'aide du schéma => TaskSchema
    task_schema = TaskSchema()
    error = task_schema.validate(request.json) # Initialisation lors de passage de la première valeur
    
    if error:
        # Si validation échoue, retourner une erreur 400
        return jsonify(error), 400
    
    # charger les données valides
    new_task = task_schema.load(request.json)
    
    # Insérer la nouvelle tâche dans mongoDB ('task')
    result = db['task'].insert_one(new_task)
    
    # Ajouter l'id MonhgoDb généré dans la réponse
    new_task['id'] = str(result.inserted_id)
    
    # Sérialisation la nouvelle tâche pour la réponse en JSON
    task_serialized = task_schema.dump(new_task)
    
    # Renvoie la tâche crée sour forme de JSON avec un code 201 => Création reussie
    return jsonify(task_serialized), 201

# Update : Mise à jour d'une tache
def update(id):
    return jsonify(f"Id récupéré lors de l'update => {id}"), 200

# Delete : Suppression d'une tâche