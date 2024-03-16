from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "super-secret"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    user = db.Column(db.String(50))
    role = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.name}>'


with app.app_context():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(name=request.json['user'], password=request.json['password']).first()
    if user:
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role, "name": user.name, "email": user.email, "user": user.user})
        return jsonify({"message": "Login succeeded", "token": access_token})
    else:
        return jsonify({"message": "Bad username or password"}), 401


@app.route('/users', methods=['POST'])
def create_user():
    new_user = User(
        name=request.json['name'],
        email=request.json['email'],
        user=request.json['user'],
        password=request.json['password'],
        role=request.json['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email, "role": new_user.role}})


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email, "role": user.role} for user in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "role": user.role})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/users/<string:user>', methods=['GET'])
def get_user_by_user(user):
    user = User.query.filter_by(user=user).first()
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "role": user.role})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        data = request.json
        user.update(data)
        return jsonify({"message": "User updated", "user": user})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"})


@app.route('/ping', methods=['GET'])
def index():
    return jsonify("users ok")


if __name__ == '__main__':
    jwt = JWTManager(app)
    app.run(debug=True)
