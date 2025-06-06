from flask import session, request
from app.controllers.controller import BaseController
from app.models.Action import Action

base = BaseController()

def record_view(request, post_id=None):
    user_id = session.get('user_id')
    if not user_id:
        return base.error_response("Login required", 401)

    if post_id is None:
        # 如果不是從 URL 傳進來，就從 body 取
        data = request.get_json()
        post_id = data.get('post_id') if data else None

    if not post_id:
        return base.error_response("post_id is required", 400)

    Action.record(user_id, post_id, 'view', deduplicate=True)
    return base.success_response("View recorded")

