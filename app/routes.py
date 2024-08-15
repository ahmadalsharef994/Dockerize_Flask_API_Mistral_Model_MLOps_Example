from flask import request, jsonify, render_template_string
from . import db
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint

bp = Blueprint('routes', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Bad credentials"), 401

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@bp.route('/hello', methods=['GET'])
def hello():
    return render_template_string('<h1>Hello, World 2!</h1>')

def init_app(app):
    app.register_blueprint(bp)
