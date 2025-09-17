
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
經過Reinforcement Learning Intuition推薦的演算等價於一個 互動偏好 80 % ＋ 隨機探索 20 % 「多臂機器賭博機（Multi-Armed Bandit）」問題：
類比增強學習的 4 大元素
元件  你系統中的實作
🟦 狀態 (State)   使用者最近互動紀錄構成狀態向量：
• top_tags（7 天內偏好主題）
• recent_view_tags（近 1 天看過主題）
• last_active_minutes（使用者活躍度）
🟩 行動 (Action)  推薦某一篇貼文的 post_id（一次回傳 k 篇）
🟨 獎勵 (Reward)  使用者實際行為：
• view +0.1
• like +1.0
• comment +1.5
• share +2.0（並加入時間衰減）
🟥 策略 (Policy)  combined_score()：分數函數
• 結合 post_rewards, tag_rewards, bonus
• 排序後推薦前 k 篇貼文
🔁 TagAwareBandit：推薦流程（策略學習角度）
1. 獲得狀態：建構使用者偏好
從 Action 表中分析：
近 7 天常互動的 tag → 建立 top_tags
近 1 天看過的貼文 tag → 建立 recent_view_tags
上次活躍時間 → last_active_minutes
這些組成當前的 使用者狀態 state。
 2. 決策（策略計分）：combined_score()
每篇候選貼文會計算一個分數，組成策略 π(s, a)：
互動 reward：post_rewards（like/comment 整體品質）
個人 tag reward：user_tag_rewards、fallback 全體 tag_rewards
偏好命中加分：
命中 top_tags：+0.2
命中 recent_view_tags：+0.15
已看過貼文降分：× 0.4
最後：
score = (1 - tag_weight) * post_reward + tag_weight * tag_reward + bonus
3. 採樣行動：推薦貼文
將所有貼文依分數排序後：
前 80% → 主推薦（偏好）
後 20% → 從未看過貼文隨機抽樣（探索）
系統回傳一組推薦貼文 ID，並顯示給使用者。
4. 等待回饋：獲取 Reward
使用者對推薦貼文的行為會記錄在 Action 表中（包括 view / like / comment 等）。
這些行為即為 實際 reward。
5. 策略更新：實時學習
在下一次執行 update(session) 時：
重新統計最近 30 天互動
將 reward 加總、加權、時間衰減
更新 post_rewards, tag_rewards, user_tag_rewards




前端滑動到貼文區塊時打 API 至少停留 5 秒才算 view
        G
    end

