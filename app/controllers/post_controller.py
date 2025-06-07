#controllers/post_controller.py
from app.controllers.controller import BaseController
from flask import session, request

from app.models.RecommendLog import RecommendLog
from app.models.Post import Post
from app.models.PostImage import PostImage
from app.models.Follow import Follow
from app.models.Like import Like
from app.models.Comment import Comment
from app.models.User import User
from app.models.Block import Block
from app.models.Action import Action


import os
from flask import session

base = BaseController()

def is_blocked(a_id, b_id):
    return Block.is_blocked(a_id, b_id)

def get_feed(request):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response("Login required", 401)

    # 取得使用者自己發的貼文
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()

    return base.success_response([p.to_dict() for p in posts], "Your posts loaded")

def create_post(request):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response("Login required", 401)

    if request.content_type.startswith('application/json'):
        data = base.get_json()
        content = data.get('content') if data else None
        images = None
    else:
        content = request.form.get('content')
        images = request.files.getlist('images') if request.files else None

    if not content:
        return base.error_response("Content is required", 400)

    post = Post.create_with_images(user_id, content, images)
    return base.success_response(post.to_dict(), "Post created", 201)

def update_post(request, post_id):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response("Login required", 401)

    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)
    if post.user_id != user_id:
        return base.error_response("Permission denied", 403)

    data = base.get_json()
    content = data.get('content')
    if not content:
        return base.error_response("Content is required")

    post.update_content(content)  # ✅ 負責處理 tags 更新 + commit
    return base.success_response(post.to_dict(), "Post updated")

# ▶ 刪除貼文（使用者刪自己的）
def delete_post(request, post_id):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response("Login required", 401)

    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)
    if post.user_id != user_id:
        return base.error_response("Permission denied", 403)

    post.soft_delete()  # ✅ 改這裡
    return base.success_response(message="Post hidden (soft deleted)")

# Admin 下架貼文
def admin_hide_post(request, post_id):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response("Login required", 401)

    user = User.query.get(user_id)
    if not user or not user.has_role('admin'):
        return base.error_response("Admin access only", 403)

    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)

    post.is_hidden = True
    post.save()
    return base.success_response(message="Post hidden by admin")

# moderator 下架貼文
def moderator_hide_post(request, post_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user or not user.has_any_role('moderator', 'admin'):
        return base.error_response("Moderator or Admin access only", 403)

    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)

    post.is_hidden = True
    post.save()
    return base.success_response(message="Post hidden by moderator or admin")

def like_post(request, post_id):
    user_id = session.get('user_id')
    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)
    if is_blocked(user_id, post.user_id):
        return base.error_response("You cannot like this post due to block status.")

    result = Like.toggle_reaction(user_id, post_id, 'like')

    if result == "liked":  # ✅ 只有新增讚才記錄
        Action.record(user_id, post_id, 'like')

    return base.success_response(f"Post {result}.")

def dislike_post(request, post_id):
    user_id = session.get('user_id')
    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)
    if is_blocked(user_id, post.user_id):
        return base.error_response("You cannot dislike this post due to block status.")
    
    result = Like.toggle_reaction(user_id, post_id, 'dislike')
    return base.success_response(f"Post {result}.")

def comment_post(request, post_id):
    if post_id is None:
        return base.error_response("Missing post_id in URL", 400)

    user_id = session.get('user_id')
    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)
    if is_blocked(user_id, post.user_id):
        return base.error_response("You cannot comment due to block status.")

    data = request.get_json()
    content = data.get("comment")
    parent_id = data.get("parent_id")

    if not content:
        return base.error_response("Comment text is required.")

    comment_dict = Comment.create(user_id, post_id, content, parent_id)

    # ✅ 新增行為記錄
    Action.record(user_id, post_id, 'comment')

    return base.success_response(message="Comment posted.", data=comment_dict)

def delete_comment(request, comment_id):
    user_id = session.get('user_id')
    success = Comment.delete(comment_id, user_id)  # 只是更新 is_deleted
    if success:
        return base.success_response(message="Comment marked as deleted.")
    return base.error_response("Delete failed or not owner.")

def update_comment(request, comment_id=None):
    user_id = session.get('user_id')
    data = request.get_json()
    new_content = data.get('comment')

    if not comment_id or not new_content:
        return base.error_response("Missing comment ID or content.")

    success = Comment.update(comment_id, user_id, new_content)
    if success:
        return base.success_response("Comment updated.", data={"comment_id": comment_id, "comment": new_content})
    return base.error_response("Update failed or not authorized.")

def get_comments_for_post(request, post_id):
    user_id = session.get('user_id')
    post = Post.get_by_id(post_id)
    if not post:
        return base.error_response("Post not found", 404)
    if is_blocked(user_id, post.user_id):
        return base.error_response("Cannot view comments due to block status.")

    comments = Comment.get_comments_for_post(post_id)

    for c in comments:
        if c.get("is_deleted"):  # 判斷是否被標記刪除
            c["comment"] = "這則留言已被刪除"

    return base.success_response(data=comments, message="Comments loaded.")

def recommend_post(request):
    user = User.query.get(session['user_id'])
    if not user:
        return base.error_response("User not found", 404)

    posts = Post.recommend_for_user(user)
    if not posts:
        return base.error_response("No post found", 404)

    post_dicts = [p.to_dict() for p in posts]
    return base.success_response(post_dicts, "Recommended posts")

