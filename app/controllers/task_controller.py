from bson import ObjectId
from flask import  request, jsonify
from marshmallow import ValidationError
from app.models.task_schema import TaskSchema
from app.services.connect_db import db

# définir la logique pour la communication avec la base de donnée 

# CRUD

# GetAll : Récupérer toute les tâches
def get_all():
    tasks = list(db['task'].find())
    
    task_schema = TaskSchema(many=True)
    serialized_task = task_schema.dump(tasks)
    
    return jsonify(serialized_task), 200

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
    new_task['_id'] = str(result.inserted_id)
    
    # Sérialisation la nouvelle tâche pour la réponse en JSON
    task_serialized = task_schema.dump(new_task)
    
    # Renvoie la tâche crée sour forme de JSON avec un code 201 => Création reussie
    return jsonify(task_serialized), 201

# Update : Mise à jour d'une tache
def update(id):
    
    # Valider les données de mise à jour
    task_schema = TaskSchema()
    data = request.json
    
    try:
        # Charger les données partiellement (ne pas obliger tout les champs)
        task_schema.load(data, partial=True)
    except ValidationError as error:
        # Retourner une erreur 400 si validation échoue
        return jsonify(error), 400

    # Rechercher la tâche à mettre à jour par son objectId
    task = db['task'].find_one({"_id": ObjectId(id)})
    
    if task:
        # Mettre à jour la tâche dans mongoDB avec les nouvelles données
        db['task'].update_one({"_id": ObjectId(id)}, {"$set" : data})
        
        # Récupérer la tâche mise à jour pour l'afficher dans la réponse
        updated_task = db['task'].find_one({"_id": ObjectId(id)})
        
        # Sérialiser la tâche mise à jour
        serialized_task = task_schema.dump(updated_task)
        
        # Renoie la tâche mise à jour sous forme de JSON avec un code 200 (Succès)
        return jsonify(serialized_task), 200
    else:
        # Retourner une erreur 404 si la tâche n'existe pas
        return {'message': f"Aucune tâche trouvé pour l'id ${id} "}, 404 

# Delete : Suppression d'une tâche
def delete(id):
    
    result = db['task'].delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count > 0:
        return {'message' : f"La tâche correspondant a l'id ({id}) à bien été supprimé !"}, 204
    else:
        return {'message' : f'Aucune tâche correspondant a {id}'}, 404