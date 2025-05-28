app/
├── main.py               ← 專案入口點（你原本稱 API.py）
├── routes.py             ← 註冊所有 route
├── controllers/
│   └── controller.py     ← 基底控制器
├── models/
│   ├── model.py          ← 資料庫初始化與連線設定
│   └── user.py           ← 使用者 model，繼承 model.py
├── templates/            ← HTML（若有）
├── static/               ← 前端資源
└── requirements.txt
