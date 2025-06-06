from app.models.Follow import Follow
from app.models.Block import Block
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
