from app import app
from app.controllers import task_controller

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return task_controller.get_all()

@app.route('/task/create', methods=['POST'])
def create_task():
    return task_controller.ajouter_tache()

@app.route('/task/udpate/<string:id>', methods=['POST'])
def update_task(id):
    return task_controller.update(id)

@app.route('/task/<string:id>', methods=['DELETE'])
def delete_task(id):
    return task_controller.delete(id)