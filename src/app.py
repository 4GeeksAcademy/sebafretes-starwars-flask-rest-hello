"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Listar todos los usuarios del blog.
@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()

    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())

    response_body = {
        "msg": "Ok", "result" : users_serialized
    }

    return jsonify(response_body), 200

#Listar todos los registros de people en la base de datos
@app.route('/people', methods=['GET'])
def get_characters():

    characters = Character.query.all()

    characters_serialized = []
    for char in characters:
        characters_serialized.append(char.serialize())

    response_body = {
        "msg" : "Ok",
        "result" : characters_serialized
    }

    return jsonify(response_body), 200

#Muestra la información de un solo personaje según su id.
@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_character(people_id):

    single_character = Character.query.get(people_id)
    return jsonify({
        "msg" : "Ok",
        "character" : single_character.serialize()
    }), 200

#Listar todos los registros de planets en la base de datos.
@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()

    planets_serialized = []
    for item in planets:
        planets_serialized.append(item.serialize())

    response_body = {
        "msg" : "Ok",
        "result" : planets_serialized
    }

    return jsonify(response_body), 200

#Muestra la información de un solo planeta según su id.
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    single_planet = Planet.query.get(planet_id)
    return jsonify({
        "msg" : "Ok",
        "character" : single_planet.serialize()
    }), 200


#Listar todos los favoritos que pertenecen al usuario actual.
@app.route('/users/favorites', methods=['GET'])
def user_favorite():

    userchar_favorites = FavoriteCharacter.query.all()
    userplanet_favorites = FavoritePlanet.query.all()
    result1 = list(map(lambda fav: fav.serialize(), userchar_favorites))
    result2 = list(map(lambda fav: fav.serialize(), userplanet_favorites))
    return jsonify(result1, result2), 200


#Añade un nuevo people favorito al usuario actual con el id = people_id
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_new_fav_character(people_id):

    user = User.query.first()

    if user:
        character = Character.query.get(people_id)
        if character:
            fav = FavoriteCharacter(user_id = user.id, character_id = people_id)
            db.session.add(fav)
            db.session.commit()
            return jsonify({'msg': 'Character added successfully'}), 200
        else: return jsonify({'msg': 'Character not found'}), 404
    else: return jsonify({'msg': 'User not found'}), 404


#Añade un nuevo planet favorito al usuario actual con el id = planet_id
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_fav_planet(planet_id):

    user = User.query.first()

    if user:
        planet = Planet.query.get(planet_id)
        if planet:
            fav = FavoritePlanet(user_id = user.id, planet_id = planet_id)
            db.session.add(fav)
            db.session.commit()
            return jsonify({'msg': 'Planet added successfully'}), 200
        else: return jsonify({'msg': 'Planet not found'}), 404
    else: return jsonify({'msg': 'User not found'}), 404

#Elimina un planet favorito con el id = planet_id
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    favorite = FavoritePlanet.query.get(planet_id)
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planet deleted"}),200

#Elimina un people favorito con el id = people_id
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_character(people_id):

    favorite = FavoriteCharacter.query.get(people_id)
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Character deleted"}),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
