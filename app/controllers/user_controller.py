from app.models.Follow import Follow
from app.models.Block import Block
from app.models.User import User
from app.models.Role import Role
from app.controllers.controller import BaseController

from flask import session, request

base = BaseController()

def follow_user(request, user_id):
    follower_id = session.get('user_id')
    if Follow.follow(follower_id, user_id):
        return base.success_response("Followed user.")
    return base.error_response("Already following or invalid user.")

def unfollow_user(request, user_id):
    follower_id = session.get('user_id')
    if Follow.unfollow(follower_id, user_id):
        return base.success_response("Unfollowed user.")
    return base.error_response("Not following or invalid user.")

def block_user(request, user_id):
    blocker_id = session.get('user_id')
    if not user_id or blocker_id == user_id:
        return base.error_response("Invalid block request")
    success = Block.block(blocker_id, user_id)
    if success:
        return base.success_response("User blocked.")
    return base.error_response("Already blocked or failed.")

def unblock_user(request, user_id):
    blocker_id = session.get('user_id')
    if not user_id:
        return base.error_response("Invalid unblock request")
    success = Block.unblock(blocker_id, user_id)
    if success:
        return base.success_response("User unblocked.")
    return base.error_response("Not blocked or failed.")

def get_user_info(request):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response('User not logged in', 401)

    user = User.query.get(user_id)
    if not user:
        return base.error_response('User not found', 404)

    role_name = user.role.role_name if user.role else 'unknown'
    return base.success_response({
        'username': user.username,
        'role': role_name
    })
    
def get_following_list(request):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response('User not logged in', 401)

    user = User.query.get(user_id)
    if not user:
        return base.error_response('User not found', 404)

    followee_ids = [f.followee_id for f in user.following]
    followees = User.query.filter(User.id.in_(followee_ids)).all()
    result = [{'id': u.id, 'username': u.username} for u in followees]
    return base.success_response({'following': result})

def get_follow_stats(request):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response('User not logged in', 401)

    following_count = Follow.count_following(user_id)
    follower_count = Follow.count_followers(user_id)

    return base.success_response({
        'following_count': following_count,
        'follower_count': follower_count
    })
    