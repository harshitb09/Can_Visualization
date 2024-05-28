from flask import Blueprint, logging, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, SessionLocal
from config.config import login_manager
from sqlalchemy.orm import query

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        user = session.query(User).get(int(user_id))
        return user

@auth.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("join.html")
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request format"}), 400  # Bad Request
        
        required_fields = ["firstname", "lastname", "username", "email", "phone", "password"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Extract user information
        first_name = data.get("firstname")
        last_name = data.get("lastname")
        username = data.get("username")
        email = data.get("email")
        phone_number = data.get("phone")
        password = data.get("password")

        # Check for existing username and email
        with SessionLocal() as session:
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            if existing_user:
                if existing_user.username == username:
                    return jsonify({"error": "Username already exists"}), 409 
                elif existing_user.email == email:
                    return jsonify({"error": "Email address already in use"}), 409

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create a new user object
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,  # Adjust if variable name differs
            password_hash=hashed_password
        )

        # Add user to database and commit changes
        with SessionLocal() as session:
            session.add(new_user)
            session.commit()

        return jsonify({"status": "success", "redirect": url_for("auth.login")})

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request format"}), 400  # Bad Request

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        with SessionLocal() as session:
            user = session.query(User).filter_by(username=username).first()
            if user and user.verify_password(password):
                login_user(user)
                return jsonify({"status": "success", "redirect": url_for("index")})
                #return jsonify({"status": "success", "redirect": url_for("visualization")})
            else:
                return jsonify({"error": "Invalid username or password"}), 401

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    # session.clear()
    return redirect(url_for('login')) 
