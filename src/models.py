from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username" : self.username,
            "email": self.email,
        }

    # def __repr__(self):
    #     return '<User %r>' % self.username

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Character)

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "character_id" : self.character_id,
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "planet_id" : self.planet_id
        }