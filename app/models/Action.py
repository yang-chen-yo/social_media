# app/models/Action.py

from app.models.model import db

class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    action_type = db.Column(db.Enum('view', 'like', 'comment', 'share'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @staticmethod
    def record(user_id, post_id, action_type, deduplicate=True):
        """
        建立使用者行為記錄
        :param user_id: 使用者 ID
        :param post_id: 貼文 ID（可為 None）
        :param action_type: 'view', 'like', 'comment', 'share'
        :param deduplicate: 是否避免重複寫入（view 建議為 True）
        """
        if deduplicate:
            exists = Action.query.filter_by(
                user_id=user_id,
                post_id=post_id,
                action_type=action_type
            ).first()
            if exists:
                return  # 已存在，不寫入

        action = Action(user_id=user_id, post_id=post_id, action_type=action_type)
        db.session.add(action)
        db.session.commit()
