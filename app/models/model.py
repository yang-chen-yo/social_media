from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # 不建立這個 base 類別為資料表
    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def init_db():
    from models.user import User  # 確保所有 model 都被載入再 create_all
    db.create_all()
