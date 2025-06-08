# main.py
import os
import sys
sys.dont_write_bytecode = True
from flask import Flask
from config import LocalConfig
from app.models.model import db
from app.routes import register_routes
import os
import importlib
import re


app = Flask(__name__, template_folder='app/views')
app.config.from_object(LocalConfig)

db.init_app(app)
register_routes(app)

def auto_import_models():
    models_dir = os.path.join(os.path.dirname(__file__), 'app', 'models')
    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and filename not in ('__init__.py', 'model.py'):
            module_basename = filename[:-3]
            if not re.match(r'^[a-zA-Z_]\w*$', module_basename):
                print(f"跳過非法檔名: {filename}")
                continue
            full_module_name = f"app.models.{module_basename}"
            try:
                importlib.import_module(full_module_name)
                print(f"匯入成功: {full_module_name}")
            except Exception as e:
                print(f"匯入失敗: {full_module_name}，錯誤: {e}")
                
if __name__ == '__main__':
    with app.app_context():
        auto_import_models()  # 自動載入所有 models
        db.create_all()
    try:
        print("Flask app starting at http://127.0.0.1:5000")
        app.run(host="0.0.0.0", port=5000, debug=False)
    except Exception as e:
        print(f"[ERROR] Failed to start app: {e}")