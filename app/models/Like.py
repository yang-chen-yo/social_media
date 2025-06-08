from app.models.model import db, BaseModel
from sqlalchemy import text

class Like(BaseModel):
    __tablename__ = 'likes'

    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.Enum('like', 'dislike'), default='like')
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @classmethod
    def toggle_reaction(cls, user_id, post_id, action_type):
        existing = db.session.execute(
            text("""
                SELECT action_type FROM likes
                WHERE user_id = :uid AND post_id = :pid
            """),
            {"uid": user_id, "pid": post_id}
        ).first()

        # 1. 沒有紀錄 → 新增
        if not existing:
            db.session.execute(
                text("INSERT INTO likes (user_id, post_id, action_type) VALUES (:uid, :pid, :atype)"),
                {"uid": user_id, "pid": post_id, "atype": action_type}
            )
            db.session.commit()
            return f"{action_type}d"  # liked / disliked

        # 2. 如果同樣類型 → 刪除（toggle off）
        if existing[0] == action_type:
            db.session.execute(
                text("DELETE FROM likes WHERE user_id = :uid AND post_id = :pid"),
                {"uid": user_id, "pid": post_id}
            )
            db.session.commit()
            return f"{action_type} removed"

        # 3. 否則是另一種反應 → 更新為新的
        db.session.execute(
            text("""
                UPDATE likes
                SET action_type = :atype, created_at = CURRENT_TIMESTAMP
                WHERE user_id = :uid AND post_id = :pid
            """),
            {"uid": user_id, "pid": post_id, "atype": action_type}
        )
        db.session.commit()
        return f"{action_type} switched"
    
    @classmethod
    def get_liked_post_ids(cls, user_id):
        result = db.session.execute(
            text("""
                SELECT post_id FROM likes
                WHERE user_id = :uid AND action_type = 'like'
            """),
            {"uid": user_id}
        )
        return [row[0] for row in result]
