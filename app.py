from flask import Flask, jsonify, request
import sqlite3
import re

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

#Root
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask API! Endpoints: /status, /data"}), 200


# Endpoint 1: Check server status
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "Server is running"}), 200


# Endpoint 2: Handle data via POST
@app.route('/data', methods=['POST'])
def handle_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400
    if 'name' not in data or 'role' not in data:
        return jsonify({"error": "Missing 'name' or 'role' in payload"}), 400
    return jsonify({"received_data": data}), 201


# Users Endpoint - Insert a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing 'name' or 'email' in payload"}), 400
    
    if not is_valid_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (data['name'], data['email']))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    
# Users Endpoint - Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing 'name' or 'email' in payload"}), 400
    
    if not is_valid_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET name = ?, email = ? WHERE id = ?',
            (data['name'], data['email'], user_id)
        )
        conn.commit()
        conn.close()
        
        if cursor.rowcount == 0:  # Check if any row was updated
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully!"}), 200

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

# Users Endpoint - Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        if cursor.rowcount == 0:  # Check if any row was deleted
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Users Endpoint - Fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(dict(user)), 200


if __name__ == '__main__':
    app.run(debug=True)