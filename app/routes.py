# app/routes.py
from app.controllers.auth_controller import auth
from app.controllers.post_controller import post

def register_routes(app):
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(post, url_prefix='/api/post')
