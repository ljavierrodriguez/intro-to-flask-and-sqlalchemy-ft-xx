import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db, Todo, User, Profile, Role

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
    
    return jsonify(todos), 200

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    
    todo = Todo()
    todo.title = data['title']
    todo.done = data['done']
    todo.users_id = data['users_id']
    todo.save()
    
    return jsonify(todo.serialize_with_user()), 201

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def remove_todo(id):
    #todo = db.get_or_404(Todo, id) # SQLAlchemy v3.0
    todo = Todo.query.get(id) # SQLAlchemy  v2.0 and early
    todo.delete()
    
    #db.session.delete(todo)
    #db.session.commit()
    
    return jsonify({ "id": id }), 200



@app.route('/api/users', methods=['GET'])
def list_users():
    users = User.query.all() # [<User 1>, <User 2>]
    users = list(map(lambda user: user.serialize_with_full_info(), users)) # [{"id": 1}, {"id": 2}]
    
    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def add_user():
    
    username = request.json.get('username')
    password = request.json.get('password')
    biography = request.json.get('biography', '')
    roles = request.json.get('roles')
    '''
    user = User()
    user.username = username
    user.password = password
    user.save()
    
    profile = Profile()
    profile.biography = biography
    profile.users_id = user.id
    profile.save()
    '''
    
    user = User()
    user.username = username
    user.password = password
    
    profile = Profile()
    profile.biography = biography

    for roles_id in roles:
        role = Role.query.get(roles_id)
        if role: user.roles.append(role)
    
    user.profile = profile # Asociamos a traves del relationship
    user.save()
    
    return jsonify(user.serialize_with_full_info()), 201


@app.route('/api/roles/<int:id>', methods=['GET'])
def show_role(id):
    role = Role.query.get(id)
    users = list(map(lambda user: user.username, role.users))
    info = {
        "role": role.serialize()
    }
    info["users"] = users
   
    return jsonify(info), 200

# crear tablas al iniciar la aplicacion
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()