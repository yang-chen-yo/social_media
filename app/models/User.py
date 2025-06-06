#models/User.py
from app.models.model import db, BaseModel

class User(BaseModel):  
    __tablename__ = 'users'

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    
    blocking = db.relationship(
        'Block',
        primaryjoin="User.id == Block.blocker_id",
        backref='blocker',
        lazy='dynamic'
    )

    blocked_by = db.relationship(
        'Block',
        primaryjoin="User.id == Block.blocked_id",
        backref='blocked',
        lazy='dynamic'
    )
    
        # ✅ 使用者追蹤了誰
    following = db.relationship(
        'Follow',
        primaryjoin="User.id == Follow.follower_id",
        backref='follower',
        lazy='dynamic'
    )

    # ✅ 使用者被誰追蹤
    followers = db.relationship(
        'Follow',
        primaryjoin="User.id == Follow.followee_id",
        backref='followee',
        lazy='dynamic'
    )

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
