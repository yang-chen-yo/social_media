from app.models.model import db, BaseModel

class PostImage(BaseModel):
    __tablename__ = 'post_images'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
