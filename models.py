from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# ondelete="CASCADE" permite borrar todos los registros relacionados a la tabla padre cuando borran el registro principal
roles_users = db.Table('roles_users', 
    db.Column('roles_id', db.Integer, db.ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),                    
    db.Column('users_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)                       
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)
    profile = db.relationship('Profile', cascade="all, delete", uselist=False, backref="user") # [<Profile 1>] => <Profile 1> # 1 - 1
    todos = db.relationship('Todo', back_populates="user", lazy=True)
    roles = db.relationship('Role', cascade="all, delete", secondary=roles_users, backref="users")
    
    # cascade="all, delete" permite borrar toda la informacion relacionada cuando eliminan el registro principal
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        
    def serialize_with_profile(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "profile": self.profile.serialize()
        }
        
    def serialize_with_full_info(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "profile": self.profile.serialize(),
            "todos": self.get_todos(),
            "roles": self.get_roles()
        }
    
    def get_todos(self):
        return list(map(lambda todo: todo.serialize(), self.todos)) #[{"id": 1}, {"id": 2}]
    
    def get_roles(self):
        return list(map(lambda role: role.serialize(), self.roles))
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.Text(), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "biography": self.biography
        }
        
    def serialize_with_user(self):
        return {
            "id": self.id,
            "biography": self.biography,
            "users_id": self.users_id,
            "user": self.user.username
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean(), default=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)
    user = db.relationship('User', back_populates="todos", lazy=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
    def serialize_with_user(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": self.user.username
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()