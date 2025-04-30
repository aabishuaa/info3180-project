# Add any model classes for Flask-SQLAlchemy here
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    photo = db.Column(db.String(255))  
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profiles = db.relationship('Profile', backref='user', lazy=True)
    favorites = db.relationship('Favourite', foreign_keys='Favourite.user_id_fk', backref='user', lazy=True)

    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __init__(self, username, password, name, email, photo=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        self.photo = photo

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'

class Profile(db.Model):
    __tablename__ = 'profile'  

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    parish = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.String(512), nullable=False)
    sex = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(80), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    fav_cuisine = db.Column(db.String(120), nullable=False)
    fav_colour = db.Column(db.String(80), nullable=False)
    fav_school_subject = db.Column(db.String(80), nullable=False)
    political = db.Column(db.Boolean, default=False)
    religious = db.Column(db.Boolean, default=False)
    family_oriented = db.Column(db.Boolean, default=False)

    # Relationships
    favorites = db.relationship('Favourite', foreign_keys='Favourite.fav_user_id_fk', backref='profile', lazy=True)

    def __init__(self, user_id_fk, description, parish, biography, sex, race, birth_year, height, 
                 fav_cuisine, fav_colour, fav_school_subject, political=False, 
                 religious=False, family_oriented=False):
        self.user_id_fk = user_id_fk
        self.description = description
        self.parish = parish
        self.biography = biography
        self.sex = sex
        self.race = race
        self.birth_year = birth_year
        self.height = height
        self.fav_cuisine = fav_cuisine
        self.fav_colour = fav_colour
        self.fav_school_subject = fav_school_subject
        self.political = political
        self.religious = religious
        self.family_oriented = family_oriented

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Profile {self.id} for User {self.user_id_fk}>'

class Favourite(db.Model):
    __tablename__ = 'favourite'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure a user can't favorite the same profile multiple times
    __table_args__ = (
        db.UniqueConstraint('user_id_fk', 'fav_user_id_fk', name='unique_favourite'),
    )

    def __init__(self, user_id_fk, fav_user_id_fk):
        self.user_id_fk = user_id_fk
        self.fav_user_id_fk = fav_user_id_fk

    def __repr__(self):
        return f'<Favourite {self.id}: User {self.user_id_fk} -> Profile {self.fav_user_id_fk}>'

