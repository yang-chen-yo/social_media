# controllers/auth_controller.py
from app.controllers.controller import BaseController
from app.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, render_template


base = BaseController()

def login(request):
    data = base.get_json()
    if not data:
        return base.error_response("Missing JSON body")

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return base.error_response("Missing username or password")

    user = User.get_by_username(username)
    if user and check_password_hash(user.password, password):
        if user.role_id == 4:
            return base.error_response("Account has been banned", 403)

        session['user_id'] = user.id
        return base.success_response(user.to_dict(), message="Login successful")

    return base.error_response("Invalid credentials")

def register(request):
    data = base.get_json()
    if not data:
        return base.error_response("Missing JSON body")

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id', 2)  # 預設為 regular 使用者

    if not username or not email or not password:
        return base.error_response("Missing required fields")

    # 檢查是否已存在
    if User.get_by_username(username):
        return base.error_response("Username already exists")
    if User.get_by_email(email):
        return base.error_response("Email already exists")

    hashed_pw = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_pw, role_id=role_id)

    try:
        user.save()
        return base.success_response(user.to_dict(), message="Registration successful")
    except Exception as e:
        return base.error_response(f"DB Error: {str(e)}")


    

def logout(request):
    session.pop('user_id', None)
    return base.success_response(message="Logout successful")


