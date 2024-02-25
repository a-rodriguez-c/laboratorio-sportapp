from flask import Flask, jsonify, request

app = Flask(__name__)

#Lista en memoria para almacenar usuarios (simulando una base de datos)
users = [
{"id": 1, "username": "user1", "email": "user1@example.com"},
{"id": 2, "username": "user2", "email": "user2@example.com"}
]

#Obtener todos los usuarios

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

#Obtener un usuario por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

# Crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    new_user["id"] = len(users) + 1
    users.append(new_user)
    return jsonify({"message": "User created", "user": new_user}), 201

# Actualizar un usuario existente
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        data = request.json
        user.update(data)
        return jsonify({"message": "User updated", "user": user})
    else:
        return jsonify({"message": "User not found"}), 404

# Eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)
