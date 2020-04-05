import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import set_up_db, db, Movie, Actor
# from auth.auth import AuthError, requires_auth
from validate import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    set_up_db(app)
    CORS(app)

    # welcome route
    @app.route('/')
    def welcome():
        try:
            return "welcome to capstone movies"
        except():
            abort(500)

    #####################   ACTORS ENDPOINTS STARTS #################################################
    '''
    TODO: GET ACTOR END POINT
    '''
    # TODO: GET ACTOR END POINT
    @app.route('/actors')
    def get_all_actors(jwt):
        try:
            selection = Actor.query.order_by('id').all()
            result = [item.format for item in selection]
            if not result:
                abort(400)
            return jsonify({
                'success': True,
                'actors': result,
                'total_actors': len(Actor.query.all())
            }), 200
        except():
            abort(500)

    # Get a specific actor by ID
    '''
    @TODO: GET ACTORS BY ID
    '''
    @app.route('/actors/<int:id>')
    # @requires_auth('get:movies')
    def get_actor_by_id(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200

    # Create a new actor
    '''
    @TODO: CREATE NEW ACTOR
    '''
    @app.route('/actors', methods=['POST'])
    # @requires_auth('post:actors')
    def post_actor(jwt):
        try:
            data = request.get_json()
            name = data.get('name', '')
            age = data.get('age', '')
            gender = data.get('gender', '')

            new_actor = Actor(name=name, age=age, gender=gender)
            if validate_actor(new_actor) is False:
                abort(400)
            # check if existed
            duplicate_actor = Actor.query.filter(Actor.name == new_actor.name).all()
            if bool(duplicate_actor):
                abort(409)
            try:
                new_actor.insert()
                return jsonify({
                    'success': True,
                    'message': 'Actor added',
                    'actor': new_actor.format()
                }), 201
            except():
                abort(500)
        except():
            abort(500)

    # Edit a specific actor
    '''
    @TODO EDIT SPECIFIC ACTOR
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:actors')
    def edit_actor(jwt, id):
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        actor.name = name
        actor.age = age
        actor.gender = gender
        if validate_actor(actor) is False:
            db.session.rollback()
            abort(400)
        try:
            actor.update()
            return jsonify({
                'success': True,
                'message': 'Actor updated',
                'actor': actor.format()
            }), 200
        except():
            db.session.rollback()
            abort(500)

    # Delete a particular actor
    '''
    @TODO: DELETE PARTICULAR ACTOR
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'message': 'Actor deleted successfully',
                'actor': actor.id
            })
        except():
            db.session.rollback()
            abort(500)

    #####################    ACTORS ENDPOINTS END #################################################

    #####################    MOVIE ENDPOINTS STARTS #################################################
    '''
        @TODO: GET MOVIES END POINT
        '''
    @app.route('/movies')
    # @requires_auth('get:movies')
    def get_all_movies(jwt):
        try:
            selection = Movie.query.order_by('id').all()
            result = [item.format for item in selection]
            if not result:
                abort(400)
            return jsonify({
                'success': True,
                'actors': result,
                'total_actors': len(Movie.query.all())
            }), 200
        except():
            abort(500)

    # Get a specific actor by ID
    '''
    @TODO: GET MOVIES BY ID
    '''

    @app.route('/movies/<int:id>')
    # @requires_auth('get:movies')
    def get_movie_by_id(jwt, id):
        try:
            movie = Movie.query.get(id)

            if movie is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'actor': movie.format(),
                }), 200
        except():
            abort(500)

    #####################    MOVIE ENDPOINTS STARTS #################################################

    '''
    @TODO: create error handler 
    '''

    # handle bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Bad Request, pls check your inputs"
        }), 400

    # handle unauthorized request errors
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description,
        }), 401

    # handle forbidden requests
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "You are forbidden from accessing this resource",
        }), 403

    # handle resource not found errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    # handle server error
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong, please try again"
        }), 500

    # Not processable
    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # No such method
    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            "error": 450,
            "message": "no such method"
        }), 405

    # Resource existed
    @app.errorhandler(409)
    def duplicate_resource(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "resource existed"
        }), 409

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
