#page_controller.py
from app.controllers.controller import BaseController
from app.models.User import User
from werkzeug.security import check_password_hash
from flask import session, render_template


base = BaseController()

def view_login_page(request):
    return render_template('login.html')