
import bcrypt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from alembic import op

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    news = db.relationship('News', backref='category', lazy="dynamic", cascade="all,delete")


    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }



class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, title, content, category_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.category_id = category_id
    

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(128))  # hashed


    def __init__(self, username, password, id=None):
        self.id = id
        self.username = username
        self.set_password(password)


    def set_password(self, raw_pass):
        self.password = bcrypt.hashpw(raw_pass.encode('utf8'), bcrypt.gensalt())


    def check_password(self, raw_pass):
        return bcrypt.checkpw(raw_pass.encode('utf8'), self.password)

    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
