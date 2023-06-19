import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

todos = []

@app.route('/')
def main():
    return jsonify({ "message": "API REST WITH FLASK" }), 200

@app.route('/api/todos', methods=['GET'])
def list_todos():
    data = {
        "total": len(todos),
        "results": todos
    }
    return jsonify(data), 200

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    
    todo = {
        "title": data['title'],
        "done": data['done']
    }
    
    todos.append(todo)
    
    return jsonify(todo)

@app.route('/api/todos/<int:pos>', methods=['DELETE'])
def remove_todo(pos):
    todos.pop(pos)
    data = {
        "total": len(todos),
        "results": todos
    }
    return jsonify(data), 200


if __name__ == '__main__':
    app.run()