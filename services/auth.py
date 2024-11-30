from flask import Blueprint, request, jsonify
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extract data
    username = data.get("username")
    password = data.get("password")

    # Validation: Ensure username and password are provided
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    # Create a new user instance
    user = User(username=username)
    user.set_password(password)

    # Add to DB
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract data
    username = data.get("username")
    password = data.get("password")

    # Validation: Ensure username and password are provided
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Query for the user based on username
    user = User.query.filter_by(username=username).first()

    # Validate user credentials
    if user and user.check_password(password):
        # Return the user data after successful login
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

    # Invalid credentials
    return jsonify({"error": "Invalid username or password"}), 401
