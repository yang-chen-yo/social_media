from flask import request, session
from app.controllers.controller import BaseController
from app.models.User import User
from app.models.model import db

base = BaseController()

def is_admin():
    uid = session.get('user_id')
    user = User.query.get(uid) if uid else None
    return user and user.has_role('admin')


def ban_user(request):
    if not is_admin():
        return base.error_response("Admin only", 403)

    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.get(user_id)
    if not user:
        return base.error_response("User not found", 404)

    user.role_id = 4  # banned
    db.session.commit()
    return base.success_response(message=f"User {user.username} has been banned.")


def unban_user(request):
    if not is_admin():
        return base.error_response("Admin only", 403)

    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.get(user_id)
    if not user:
        return base.error_response("User not found", 404)

    user.role_id = 2  # regular
    db.session.commit()
    return base.success_response(message=f"User {user.username} has been unbanned.")


def set_user_role(request):
    if not is_admin():
        return base.error_response("Admin only", 403)

    data = request.get_json()
    user_id = data.get("user_id")
    role_id = data.get("role_id")

    user = User.query.get(user_id)
    if not user:
        return base.error_response("User not found", 404)

    if not role_id:
        return base.error_response("Missing role_id", 400)

    user.role_id = role_id
    db.session.commit()
    return base.success_response(message=f"User {user.username} role set to {role_id}")
