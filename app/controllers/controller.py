from flask import jsonify, request

class BaseController:
    def success_response(self, data=None, message="Success", code=200):
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
