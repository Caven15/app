from app import app
from app.controllers import task_controller


@app.route('/task/create', methods=['POST'])
def create_task():
    return task_controller.ajouter_tache()

@app.route('/task/update/<string:id>', methods=['POST'])
def update_task(id):
    return task_controller.update(id)