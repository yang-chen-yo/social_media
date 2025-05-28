from flask import Flask
from config import LocalConfig
from models.model import db
from routes import register_routes

app = Flask(__name__)
app.config.from_object(LocalConfig)

db.init_app(app)
register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
