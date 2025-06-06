# app/models/RecommendLog.py
from app.models.model import db

class RecommendLog(db.Model):
    __tablename__ = 'recommend_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recommended_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    reward = db.Column(db.Float, default=None)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
