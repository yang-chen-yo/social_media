#routes.py
import importlib
from flask import request, session
from app.controllers.controller import BaseController
from app.models.User import User
import traceback 

base = BaseController()

ROUTE_MAP = {
    'noRestriction': {
        'page/login': ('page_controller', 'view_login_page'),
        'page/register': ('page_controller', 'view_register_page'),
        
        'auth/login': ('auth_controller', 'login'),
        'auth/logout': ('auth_controller', 'logout'),
        'auth/register': ('auth_controller', 'register')
    },
    'hasLogin': {
        'page/posts': ('page_controller', 'view_posts_page'),
        
        'posts/feed': ('post_controller', 'get_feed'),
        'posts/new': ('post_controller', 'create_post'),             
        'posts/update': ('post_controller', 'update_post'),       
        'posts/delete': ('post_controller', 'delete_post'),
        
        'users/follow': ('user_controller', 'follow_user'),
        'users/unfollow': ('user_controller', 'unfollow_user'),
        'users/block': ('user_controller', 'block_user'),
        'users/unblock': ('user_controller', 'unblock_user'),
        'users/meInfo': ('user_controller', 'get_user_info'),
        
        'users/following': ('user_controller', 'get_following_list'),
        'users/follow-stats': ('user_controller', 'get_follow_stats'),
        
        'posts/like': ('post_controller', 'like_post'),
        'posts/dislike': ('post_controller', 'dislike_post'),   
        'posts/comment/new': ('post_controller', 'comment_post'), 
        'posts/recommend': ('post_controller', 'recommend_post'),
        'posts/comment/update': ('post_controller', 'update_comment'),
        'posts/comment/delete': ('post_controller', 'delete_comment'),
        'posts/comments': ('post_controller', 'get_comments_for_post'),   
        
        'actions/view': ('action_controller', 'record_view')
    },
    
    'moderatorOnly': {
        'posts/hide': ('post_controller', 'moderator_hide_post')
    },
    'adminOnly': {
        'admin/posts/hide': ('post_controller', 'admin_hide_post'),
        'admin/users/ban': ('admin_controller', 'ban_user'),
        'admin/users/unban': ('admin_controller', 'unban_user'),
        'admin/users/set-role': ('admin_controller', 'set_user_role')
    }
}

# 登入與身份檢查
def is_authenticated():
    return 'user_id' in session

def is_admin():
    uid = session.get('user_id')
    if not uid:
        return False
    user = User.query.get(uid)
    return user and user.role_id == 1

# 權限驗證邏輯抽出
def check_access(restriction_level):
    if restriction_level == 'hasLogin' and not is_authenticated():
        return base.error_response('Unauthorized. Please log in.', 403)
    if restriction_level == 'adminOnly' and not is_admin():
        return base.error_response('Admin access only.', 403)
    return None  # 通過驗證

# 主路由分派
def register_routes(app):
    @app.route('/api/<path:full_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    def route_dispatch(full_path):
        path_parts = full_path.strip('/').split('/')

        # ex: /posts/update/5
        if path_parts and path_parts[-1].isdigit():
            route_key = '/'.join(path_parts[:-1])
            resource_id = int(path_parts[-1])
        else:
            route_key = '/'.join(path_parts)
            resource_id = None

        # 查找對應 controller 與權限
        route_result = None
        for restriction, route_table in ROUTE_MAP.items():
            if route_key in route_table:
                route_result = {
                    'restriction': restriction,
                    'handler': route_table[route_key]
                }
                break

        if not route_result:
            return base.error_response(f'API "{full_path}" not found', 404)

        # 權限驗證（呼叫外部函式）
        access_error = check_access(route_result['restriction'])
        if access_error:
            return access_error

        # 動態載入 controller + 呼叫對應方法
        controller_name, func_name = route_result['handler']
        try:
            print(f"📦 嘗試載入 controller: app.controllers.{controller_name}")
            module = importlib.import_module(f'app.controllers.{controller_name}')
            print(f"🔍 嘗試呼叫函數: {func_name}")
            func = getattr(module, func_name)
            return func(request, resource_id) if resource_id is not None else func(request)

        except ModuleNotFoundError as e:
            print(f"❌ 找不到 controller 模組 '{controller_name}': {e}")
            return base.error_response(f'Controller \"{controller_name}\" not found', 404)

        except AttributeError as e:
            print(f"❌ 找不到函數 '{func_name}' in controller '{controller_name}': {e}")
            return base.error_response(f'Function \"{func_name}\" not found in controller', 404)

        except Exception as e:
            print("🔥 未預期錯誤：")
            traceback.print_exc()
            return base.error_response(f'Unexpected error: {type(e).__name__} - {str(e)}', 500)
