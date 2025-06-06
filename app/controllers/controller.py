# controllers/controller.py
from flask import jsonify, request

class BaseController:
    def success_response(self, *args, data=None, message="Success", code=200):
        if args:
            message = args[0]  # 允許傳 "Success" 當成位置參數

        return jsonify({
            "status": "success",
            "message": message,
            "data": data
        }), code

    def error_response(self, message="Error", code=400):
        return jsonify({
            "status": "error",
            "message": message
        }), code

    def get_json(self):
        try:
            return request.get_json()
        except Exception:
            return None