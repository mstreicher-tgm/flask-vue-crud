import os
import uuid

import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

TODOS = [
    {
        'id': uuid.uuid4().hex,
        'todo': 'SEW Test verbessern.',
        'assignee': 'Matthias Streicher',
        'done': True,
    },
    {
        'id': uuid.uuid4().hex,
        'todo': 'Mathe Hausübung machen.',
        'assignee': 'David Samwald',
        'done': False,
    },
    {
        'id': uuid.uuid4().hex,
        'todo': 'Mitschrift nach schreiben.',
        'assignee': 'Alexander Hold',
        'done': False,
    },
]


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/todos', methods=['GET', 'POST'])
def all_tasks():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TODOS.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done')
        })
        response_object['message'] = 'Task added!'
    else:
        response_object['todos'] = TODOS
    return jsonify(response_object)


@app.route('/todos/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def single_task(task_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_task = ''
        for task in TODOS:
            if task['id'] == task_id:
                return_task = task
        response_object['task'] = return_task
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_task(task_id)
        TODOS.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done')
        })
        response_object['message'] = 'Task updated!'
    if request.method == 'DELETE':
        remove_task(task_id)
        response_object['message'] = 'Task removed!'
    return jsonify(response_object)

def remove_task(task_id):
    for task in TODOS:
        if task['id'] == task_id:
            TODOS.remove(task)
            return True
    return False


if __name__ == '__main__':
    app.run(port=8080)
