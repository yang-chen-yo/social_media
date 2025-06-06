from app.models.model import db, BaseModel
from sqlalchemy import text

class Follow(BaseModel):
    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @classmethod
    def get_followee_ids(cls, user_id):
        result = db.session.execute(
            text("SELECT followee_id FROM follows WHERE follower_id = :uid"),
            {"uid": user_id}
        )
        return [row[0] for row in result]

    @classmethod
    def count_followers(cls, user_id):
        result = db.session.execute(
            text("SELECT COUNT(*) FROM follows WHERE followee_id = :uid"),
            {"uid": user_id}
        )
        return result.scalar()

    @classmethod
    def count_following(cls, user_id):
        result = db.session.execute(
            text("SELECT COUNT(*) FROM follows WHERE follower_id = :uid"),
            {"uid": user_id}
        )
        return result.scalar()

    @classmethod
    def follow(cls, follower_id, followee_id):
        if follower_id == followee_id:
            return False
        exists = db.session.execute(
            text("""
                SELECT 1 FROM follows
                WHERE follower_id = :fid AND followee_id = :tid
            """),
            {"fid": follower_id, "tid": followee_id}
        ).first()
        if exists:
            return False
        db.session.execute(
            text("""
                INSERT INTO follows (follower_id, followee_id)
                VALUES (:fid, :tid)
            """),
            {"fid": follower_id, "tid": followee_id}
        )
        db.session.commit()
        return True

    @classmethod
    def unfollow(cls, follower_id, followee_id):
        result = db.session.execute(
            text("""
                DELETE FROM follows
                WHERE follower_id = :fid AND followee_id = :tid
            """),
            {"fid": follower_id, "tid": followee_id}
        )
        db.session.commit()
        return result.rowcount > 0
