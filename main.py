import json
from functools import wraps
import jwt
from flask import Flask, jsonify, request, Response, make_response, session
from db import *
from waitress import serve
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(testing: bool = True):
    app = Flask(__name__)


    app.config['SECRET_KEY'] = 'ca9498317b9cd8654b62666a368e0500a8f6a1161093f19bb2edfc5642e474b8'

    def admin_token_required(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = request.headers.get('token')
            if not token:
                return jsonify({'Message': 'No token provided'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
                isAdmin = data.get("admin")
                if not(isAdmin):
                    return jsonify({'Message': 'Admin access only!'}), 403
            except jwt.InvalidTokenError:
                return jsonify({'Message': 'Invalid token. Please log in again.'}), 403
            except:
                return jsonify({'Message': 'Invalid token'}), 403

            return func(*args, **kwargs)

        return decorated

    #SWAGGER
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


    def dump_or_404(data, Schema):
        if data == 404:
            return Response("Invalid ID", status=404)
        else:
            if isinstance(data, list):
                return jsonify(Schema.dump(data, many=True))
            return jsonify(Schema.dump(data))

    #Book functions
    @app.route("/book", methods=['POST'])
    @admin_token_required
    def post_book():
        book_json = BookSchema().load(request.get_json())
        book_object = Book(**book_json)

        response = Book.post_book(book_object)
        return Response(f"Status: {response}", status=response)

    @app.route("/book/<id>", methods=['PUT'])
    @admin_token_required
    def update_book(id):
        fields = BookSchema().load(request.get_json(), partial=True)
        response = Book.update_book(id, fields)
        return Response(f"Status: {response}", status=response)

    @app.route("/books/findByStatus", methods=['GET'])
    def get_book_by_status(status):
        response = Book.get_book_by_status(status)
        return dump_or_404(response, BookSchema())

    @app.route("/books/findByGenre", methods=['GET'])
    def get_book_by_genre(genre):
        response = Book.get_book_by_genre(genre)
        return dump_or_404(response, BookSchema())
        
    @app.route("/books/{bookId}", methods=['GET'])
    def get_book_by_id(id):
        response = Book.get_book_by_id(id)
        return dump_or_404(response, BookSchema())

    @app.route("/books/{author}", methods=['GET'])
    def get_book_by_author(id):
        response = Book.get_book_by_author(id)
        return dump_or_404(response, BookSchema())

    @app.route("/books/{bookName}", methods=['GET'])
    def get_book_by_name(id):
        response = Book.get_book_by_name(id)
        return dump_or_404(response, BookSchema())

    @app.route("/books", methods=['GET'])
    def get_all_books():
        response = Book.get_books()
        return jsonify(BookSchema().dump(response, many=True))

    @app.route("/book/<id>", methods=['DELETE'])
    @admin_token_required
    def delete_book(id):
        response = Book.delete_book(id)
        return Response(f"Status: {response}" , status=response)

    @app.route("/admin", methods = ["POST"])
    def log_in():
        admin_json = request.get_json()
        admin = Admin.auth(admin_json['username'], admin_json['token'])
        if admin:
            session['logged_in'] = True

            token = jwt.encode({
                'admin': admin_json['username']
            }, app.config['SECRET_KEY'])
            admin.token = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            return jsonify(AdminSchema().dump(admin))
    return app

if __name__ == '__main__':
    create_app().run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True, port=4000)
#     serve(app)
