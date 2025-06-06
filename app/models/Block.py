# models/block.py
from app.models.model import db, BaseModel
from sqlalchemy import text

class Block(BaseModel):
    __tablename__ = 'blocks'

    blocker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blocked_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @classmethod
    def block(cls, blocker_id, blocked_id):
        if blocker_id == blocked_id:
            return False
        exists = db.session.execute(
            text("SELECT 1 FROM blocks WHERE blocker_id = :bid AND blocked_id = :uid"),
            {"bid": blocker_id, "uid": blocked_id}
        ).first()
        if exists:
            return False
        db.session.execute(
            text("INSERT INTO blocks (blocker_id, blocked_id) VALUES (:bid, :uid)"),
            {"bid": blocker_id, "uid": blocked_id}
        )
        db.session.commit()
        return True

    @classmethod
    def unblock(cls, blocker_id, blocked_id):
        result = db.session.execute(
            text("DELETE FROM blocks WHERE blocker_id = :bid AND blocked_id = :uid"),
            {"bid": blocker_id, "uid": blocked_id}
        )
        db.session.commit()
        return result.rowcount > 0

    @classmethod
    def is_blocked(cls, user1_id, user2_id):
        result = db.session.execute(
            text("""
                SELECT 1 FROM blocks
                WHERE (blocker_id = :u1 AND blocked_id = :u2)
                   OR (blocker_id = :u2 AND blocked_id = :u1)
            """),
            {"u1": user1_id, "u2": user2_id}
        )
        return bool(result.first())