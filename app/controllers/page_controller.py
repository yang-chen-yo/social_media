#page_controller.py
from app.controllers.controller import BaseController
from app.models.User import User
from werkzeug.security import check_password_hash
from flask import session, render_template


base = BaseController()

def view_login_page(request):
    return render_template('login.html')

def view_register_page(request):
    return render_template('register.html')

def view_posts_page(request):
    return render_template('posts.html')

def view_users_page(request):
    return render_template('users.html')