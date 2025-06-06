#models/Comment.py
from app.models.model import db, BaseModel
from sqlalchemy import text

class Comment(BaseModel):
    __tablename__ = 'comments'

    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @classmethod
    def create(cls, user_id, post_id, content, parent_id=None):
        db.session.execute(
            text("""
                INSERT INTO comments (user_id, post_id, comment, parent_id)
                VALUES (:uid, :pid, :comment, :parent)
            """),
            {"uid": user_id, "pid": post_id, "comment": content, "parent": parent_id}
        )
        db.session.commit()
        return {"user_id": user_id, "post_id": post_id, "comment": content, "parent_id": parent_id}

    @classmethod
    def delete(cls, comment_id, user_id):
        result = db.session.execute(
            text("""
                UPDATE comments
                SET is_deleted = 1
                WHERE id = :cid AND user_id = :uid
            """),
            {"cid": comment_id, "uid": user_id}
        )
        db.session.commit()
        return result.rowcount > 0


    
    @classmethod
    def update(cls, comment_id, user_id, new_content):
        result = db.session.execute(
            text("""
                UPDATE comments
                SET comment = :content
                WHERE id = :cid AND user_id = :uid  
            """),
            {"cid": comment_id, "uid": user_id, "content": new_content}
        )
        db.session.commit()
        return result.rowcount > 0
    
    @classmethod
    def get_comments_for_post(cls, post_id):
        result = db.session.execute(
            text("""
                SELECT c.id, c.comment, c.user_id, c.parent_id, c.created_at,
                    c.is_deleted, u.username
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = :pid
                ORDER BY c.created_at ASC
            """),
            {"pid": post_id}
        )
        return [dict(row) for row in result.mappings().all()]

