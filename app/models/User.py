#models/User.py
from app.models.model import db, BaseModel

class User(BaseModel):  
    __tablename__ = 'users'

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
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
    
    def has_role(self, role_name: str) -> bool:
        return self.role and self.role.role_name == role_name

    def has_any_role(self, *role_names) -> bool:
        return self.role and self.role.role_name in role_names
    
    def to_safe_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role_id": self.role_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
