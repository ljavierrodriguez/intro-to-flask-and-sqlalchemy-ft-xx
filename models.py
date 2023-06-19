from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)
    profile = db.relationship('Profile', uselist=False, backref="user") # [<Profile 1>] => <Profile 1> # 1 - 1
    todos = db.relationship('Todo', back_populates="user", lazy=True)
    
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
            "todos": self.get_todos()
        }
    
    def get_todos(self):
        return list(map(lambda todo: todo.serialize(), self.todos)) #[{"id": 1}, {"id": 2}]
        
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
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
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