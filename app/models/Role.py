# app/models/Role.py

from app.models.model import db, BaseModel

class Role(BaseModel):
    __tablename__ = 'roles'

    role_name = db.Column(db.String(50), nullable=False)

    # 如果你想要讓角色能夠反查擁有此角色的使用者
    users = db.relationship('User', backref='role', lazy='dynamic')