sHrf4x)Rp4MqPF7T
![Untitled](https://github.com/user-attachments/assets/4c04b520-027f-4a3b-ae83-22e5d3a88f3d)

![image](https://github.com/user-attachments/assets/3401e3c2-e0e0-4416-b922-7713179f5d4b)

若 A 封鎖 B → A 看不到 B，B 看不到 A

若 A 封鎖 B → 追蹤按鈕 disabled

若 A 嘗試留言 B 的貼文 → 顯示錯誤

若 A 嘗試訪問 B 的個人頁 → 顯示「使用者不存在或不可查看」

| API 路徑               | 方法   | 說明       |
| -------------------- | ---- | -------- |
| `/api/page/login`    | GET  | 登入頁面（可選） |
| `/api/auth/login`    | POST | 使用者登入    |
| `/api/auth/logout`   | POST | 使用者登出    |
| `/api/auth/register` | POST | 使用者註冊    |
| API 路徑                   | 方法     | 說明       | 📌 是否需 ID   |
| ------------------------ | ------ | -------- | ----------- |
| `/api/posts/feed`        | GET    | 取得追蹤者的貼文 | ❌           |
| `/api/posts`             | POST   | 建立新貼文    | ❌           |
| `/api/posts/update/<id>` | PUT    | 編輯貼文內容   | ✅ `post_id` |
| `/api/posts/delete/<id>` | DELETE | 刪除貼文     | ✅ `post_id` |
| API 路徑                     | 方法   | 說明      | 📌 是否需 ID   |
| -------------------------- | ---- | ------- | ----------- |
| `/api/users/follow/<id>`   | POST | 追蹤某個使用者 | ✅ `user_id` |
| `/api/users/unfollow/<id>` | POST | 取消追蹤    | ✅ `user_id` |
| `/api/users/block/<id>`    | POST | 封鎖某個使用者 | ✅ `user_id` |
| `/api/users/unblock/<id>`  | POST | 取消封鎖    | ✅ `user_id` |
| API 路徑                           | 方法     | 說明           | 📌 是否需 ID      |
| -------------------------------- | ------ | ------------ | -------------- |
| `/api/posts/like/<id>`           | POST   | 對貼文按讚        | ✅ `post_id`    |
| `/api/posts/dislike/<id>`        | POST   | 對貼文按倒讚       | ✅ `post_id`    |
| `/api/posts/comment/new/<id>`    | POST   | 發布留言（支援巢狀留言） | ✅ `post_id`    |
| `/api/posts/comment/update/<id>` | PUT    | 修改留言內容       | ✅ `comment_id` |
| `/api/posts/comment/delete/<id>` | DELETE | 刪除留言         | ✅ `comment_id` |
| `/api/posts/comments/<id>`       | GET    | 查詢某貼文的所有留言   | ✅ `post_id`    |

| API 路徑                       | 方法   | 說明      | 📌 是否需 ID   |
| ---------------------------- | ---- | ------- | ----------- |
| `/api/admin/posts/hide/<id>` | POST | 管理員下架貼文 | ✅ `post_id` |


🧠 增強式學習思想（Reinforcement Learning Intuition）
推薦系統等價於一個「多臂機器賭博機（Multi-Armed Bandit）」問題：

每個貼文是一個「賭博機器」

使用者互動行為（點讚、留言等）回傳「獎勵（reward）」

系統透過這些獎勵學習哪些貼文更值得推薦

🎁Reward 設計
使用者與貼文的互動會轉化為對該貼文的「reward」值，對所有貼文與 tag 累積。

行為	Reward 值
view (瀏覽)	0.1
like (按讚)	1.0
comment (留言)	1.5
share (分享)	2.0

📌 加分機制說明：追蹤與留言互動
在貼文分數的計算中，若該貼文屬於下列情況之一，會額外 +0.5 分獎勵：

該貼文由使用者「追蹤」的對象所發布

該貼文曾經被使用者「追蹤者」留言互動過

🧾State 表徵（狀態設計）
這裡狀態特徵概念：

每篇貼文的歷史 reward

每個 tag 的平均 reward

使用者追蹤者、留言過的貼文（作為優先推薦因子）


🔀 Epsilon-Greedy 策略
推薦邏輯採用 ε-greedy 策略：

機率 ε（例如 10%）進行探索：隨機推薦

否則執行 exploitation：根據 reward 計算分數推薦最高分的貼文

🔍 推薦流程
排除使用者封鎖的對象 & 自己的貼文

準備所有候選貼文與其 tag

分類「追蹤者貼文」「留言過貼文」為優先推薦對象（加分）

若進行 exploitation，計算所有候選貼文的分數並排序取前 k 筆

回傳推薦結果

前端滑動到貼文區塊時打 API 至少停留 N 秒才算 view
