from app.models.model import db, BaseModel
from datetime import datetime
from sqlalchemy import not_
from app.models.Block import Block
from sqlalchemy import text
from app.models.Tag import Tag
from app.models.PostTag import PostTag
from app.models.PostImage import PostImage
from werkzeug.utils import secure_filename
from app.utils.recommend_bandit import extract_tags

import os
from sqlalchemy.exc import IntegrityError

class Post(BaseModel):
    __tablename__ = 'posts'

    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('PostImage', backref='post', lazy=True) #一對多關聯：每篇貼文對應多張圖片

    def to_dict(self):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        base_url = os.getenv("IMAGE_BASE_URL", "/static/images/")
        data['images'] = [base_url + img.image_path for img in self.images]
        return data

    @classmethod
    def get_follow_posts(cls, followee_ids):
        return cls.query.filter(
            cls.user_id.in_(followee_ids),
            cls.is_hidden == False
        ).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_recommended_posts(cls, exclude_ids, limit=5):
        return cls.query.filter(
            not_(cls.user_id.in_(exclude_ids)),
            cls.is_hidden == False
        ).order_by(db.func.rand()).limit(limit).all()
        
    @classmethod
    def create_by_user_id(cls, user_id, content):
        post = cls(user_id=user_id, content=content)
        db.session.add(post)
        db.session.flush()  # 拿到 post.id
        post.attach_tags_from_content()  # 自動從內容建立 tag 關聯
        return post
    
    def attach_tags_from_content(self):
        tags = extract_tags(self.content)
        for tag_name in tags:
            tag = Tag.query.filter_by(tag_name=tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name)
                db.session.add(tag)
                try:
                    db.session.flush()
                except IntegrityError:
                    db.session.rollback()
                    continue
            db.session.add(PostTag(post_id=self.id, tag_id=tag.id))
    
    @classmethod
    def get_by_id(cls, post_id):
        return cls.query.get(post_id)

    @classmethod
    def get_by_user_ids(cls, user_ids):
        if not user_ids:
            return []
        return cls.query.filter(
            cls.user_id.in_(user_ids),
            cls.is_hidden == False
        ).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_all_visible(cls):
        return cls.query.filter_by(is_hidden=False).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def create_with_images(cls, user_id, content, images):
        post = cls(user_id=user_id, content=content)
        db.session.add(post)
        db.session.flush()
        post.attach_tags_from_content()

        # ✅ 處理圖片（圖片可為 None）
        if images:
            upload_folder = os.getenv("UPLOAD_FOLDER", "static/images/")
            os.makedirs(upload_folder, exist_ok=True)
            for img in images:
                if img and img.filename:
                    filename = secure_filename(img.filename)
                    img.save(os.path.join(upload_folder, filename))
                    pi = PostImage(post_id=post.id, image_path=filename)
                    db.session.add(pi)

        db.session.commit()
        return post
    
    def update_content(self, new_content):
        self.content = new_content

        # 刪除舊有 tag 關聯
        PostTag.query.filter_by(post_id=self.id).delete()
        tags = extract_tags(new_content)
        for tag_name in tags:
            tag = Tag.query.filter_by(tag_name=tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name)
                db.session.add(tag)
                try:
                    db.session.flush()
                except IntegrityError:
                    db.session.rollback()
                    continue
            db.session.add(PostTag(post_id=self.id, tag_id=tag.id))
        
        self.save()  # 含 db.session.commit()

    @classmethod
    def recommend_for_user(cls, user,k=15):
        from app.utils.recommend_bandit import bandit_recommender
        bandit_recommender.update(db.session)

        sorted_ids = bandit_recommender.recommend_all(user, db.session, k)
        if not sorted_ids:
            return []

        post_map = {post.id: post for post in Post.query.filter(Post.id.in_(sorted_ids)).all()}
        return [post_map[pid] for pid in sorted_ids if pid in post_map]
