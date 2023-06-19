import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db, Todo

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASEURI')

db.init_app(app)

@app.route('/')
def main():
    return jsonify({ "message": "API REST WITH FLASK" }), 200

@app.route('/api/todos', methods=['GET'])
def list_todos():
    todos = Todo.query.all() # [<Todo 1>, <Todo 2>]
    
    print(todos)
    todos = list(map(lambda todo: todo.serialize(), todos)) # [{"id": 1}, {"id": 2}]
    print(todos)
    
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    
    todo = Todo()
    todo.title = data['title']
    todo.done = data['done']
    todo.save()
    
    return jsonify(todo.serialize()), 201

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def remove_todo(id):
    #todo = db.get_or_404(Todo, id) # SQLAlchemy v3.0
    todo = Todo.query.get(id) # SQLAlchemy  v2.0 and early
    todo.delete()
    
    #db.session.delete(todo)
    #db.session.commit()
    
    return jsonify({ "id": id }), 200

# crear tablas al iniciar la aplicacion
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()