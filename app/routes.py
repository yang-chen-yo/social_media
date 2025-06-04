# routes.py
import importlib
from flask import request
from app.controllers.controller import BaseController

base = BaseController()

ROUTE_MAP = {
    'noRestriction': {
        'page/login': ('page_controller', 'view_login_page'), 
         
        'auth/login': ('auth_controller', 'login'),               
        'auth/logout': ('auth_controller', 'logout'),
        'auth/register': ('auth_controller', 'register')
    },
    'hasLogin': {
        
    }
}

def is_authenticated():
    return 'user_id' in session

def find_route(path):
    """
    根據 path 找出對應的 controller 與 function，以及權限需求
    傳回格式：{'restriction': 'noRestriction' or 'hasLogin', 'handler': (controller, function)}
    """
    for restriction, route_table in ROUTE_MAP.items():
        if path in route_table:
            return {
                'restriction': restriction,
                'handler': route_table[path]
            }
    return None


def register_routes(app):

    @app.route('/api/<path:full_path>', methods=['GET', 'POST'])
    def route_dispatch(full_path):
        route_result = find_route(full_path)
        if not route_result:
            return base.error_response(f'API "{full_path}" not found', 404)

        restriction = route_result['restriction']
        handler = route_result['handler']

        if restriction == 'hasLogin' and not is_authenticated():
            return base.error_response('Unauthorized access. Please log in.', 403)

        controller_name, func_name = handler

        try:
            module = importlib.import_module(f'app.controllers.{controller_name}')
            func = getattr(module, func_name)
            return func(request)
        except ModuleNotFoundError:
            return base.error_response(f'Controller "{controller_name}" not found', 404)
        except AttributeError:
            return base.error_response(f'Function "{func_name}" not found in controller', 404)
        except Exception as e:
            return base.error_response(f'Unexpected error: {str(e)}', 500)
