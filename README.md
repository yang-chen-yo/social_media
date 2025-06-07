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

略的 4 大構成（對應 RL 架構）
元件	你系統中的實作
🟦 狀態 (state)	使用者的近期互動紀錄組成狀態向量：top_tags, last_active
🟩 行動 (action)	推薦一篇貼文（post_id）作為推薦決策
🟨 獎勵 (reward)	使用者對該貼文的實際行為：view(+0.1)、like(+1.0)...等
🟥 策略 (policy)	combined_score() 分數函數 → 排序後推薦 top-k 貼文

 演算法核心：TagAwareBandit
一種模仿多臂賭博機（Multi-Armed Bandit）策略的簡化推薦方法：
🔁 你的推薦策略的工作流程（策略學習角度）
獲得狀態：
從 Action 表中讀取使用者最近互動，提取 top_tags 當作偏好狀態

決策（策略）：
根據 combined_score() 函式，計算每篇貼文的分數：

互動 reward（like/comment/share/view）

個人化 tag reward（user_tag_rewards）

狀態命中加分（偏好 tag 命中）

曾看過的貼文分數打折

採樣行動（推薦貼文）：
回傳排序前 k 篇貼文 → 顯示給使用者

等待回饋（獎勵）：
使用者是否對推薦內容有互動（like/view/share 等）→ 儲存在 actions 表

系統更新策略：
在下一次 update() 時會重新計算貼文 / 標籤的 reward 分數 → 策略即時更新

前端滑動到貼文區塊時打 API 至少停留 N 秒才算 view
