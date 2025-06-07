# app/models/Action.py

from app.models.model import db
from datetime import datetime, timedelta

class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    action_type = db.Column(db.Enum('view', 'like', 'comment', 'share'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @staticmethod
    def record(user_id, post_id, action_type, deduplicate=True, interval_minutes=10):
        if deduplicate:
            now = datetime.utcnow()
            cutoff = now - timedelta(minutes=interval_minutes)

            exists = Action.query.filter_by(
                user_id=user_id,
                post_id=post_id,
                action_type=action_type
            ).filter(Action.timestamp > cutoff).first()

            if exists:
                return  # 不重複寫入

        action = Action(user_id=user_id, post_id=post_id, action_type=action_type)
        db.session.add(action)
        db.session.commit()