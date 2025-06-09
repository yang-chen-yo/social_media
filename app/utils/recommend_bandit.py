from __future__ import annotations

import re, random
from collections import defaultdict
from statistics import mean
from typing import Dict, List, Set
from datetime import datetime, timedelta

from app.models.model import db
from app.models.Action import Action
from app.models.Tag import Tag
from app.models.PostTag import PostTag
from app.models.Comment import Comment
from app.models.Follow import Follow
from app.models.Like import Like

REWARD_MAPPING: Dict[str, float] = {
    "view": 0.1,
    "like": 1.0,
    "comment": 1.5,
    "share": 2.0,
}
DEFAULT_EPSILON = 0.1
TAG_WEIGHT = 0.5

_TAG_PATTERN = re.compile(r"#(\w+)")


def extract_tags(text: str) -> Set[str]:
    return {m.group(1).lower() for m in _TAG_PATTERN.finditer(text)}


class TagAwareBandit:
    def __init__(self, epsilon: float = DEFAULT_EPSILON, tag_weight: float = TAG_WEIGHT):
        self.epsilon = epsilon
        self.tag_weight = tag_weight
        self._post_rewards: Dict[int, List[float]] = defaultdict(list)
        self._tag_rewards: Dict[str, List[float]] = defaultdict(list)
        self._user_tag_rewards: Dict[int, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))

    def update(self, session):
        self._post_rewards.clear()
        self._tag_rewards.clear()
        self._user_tag_rewards.clear()

        post_tags: Dict[int, List[str]] = defaultdict(list)
        for pid, tname in (session.query(PostTag.post_id, Tag.tag_name)
                           .join(Tag, PostTag.tag_id == Tag.id).all()):
            post_tags[pid].append(tname)

        cutoff = datetime.utcnow() - timedelta(days=30)
        for uid, pid, act, ts in (session.query(Action.user_id, Action.post_id,
                                                Action.action_type, Action.timestamp)
                                  .filter(Action.timestamp > cutoff).all()):
            if pid is None:
                continue
            w = REWARD_MAPPING.get(act, 0.0) * 0.95 ** ((datetime.utcnow() - ts).days)
            self._post_rewards[pid].append(w)
            for t in post_tags.get(pid, []):
                self._tag_rewards[t].append(w)
                self._user_tag_rewards[uid][t].append(w)

    def recommend_all(self, user, session, k: int = 30,
                      explore_ratio: float = 0.2) -> List[int]:
        from app.models.Post import Post

        cutoff = datetime.utcnow() - timedelta(days=30)

        viewed_post_ids = {pid for pid, in session.query(Action.post_id)
                           .filter(Action.user_id == user.id,
                                   Action.action_type == 'view',
                                   Action.timestamp > cutoff)}

        # ✅ 互動過的貼文：like / comment / share
        liked_post_ids = {
            pid for pid, in session.query(Like.post_id)
            .filter(Like.user_id == user.id,
                    Like.created_at > cutoff)
        }

        commented_post_ids = {
            pid for pid, in session.query(Comment.post_id)
            .filter(Comment.user_id == user.id,
                    Comment.created_at > cutoff)
        }

        shared_post_ids = {
            pid for pid, in session.query(Action.post_id)
            .filter(Action.user_id == user.id,
                    Action.action_type == 'share',
                    Action.timestamp > cutoff)
        }

        interacted_post_ids = liked_post_ids | commented_post_ids | shared_post_ids

        blocked_users = {b.blocked_id for b in user.blocking.all()} \
                        | {b.blocker_id for b in user.blocked_by.all()}

        candidate_rows = session.query(Post.id, Post.user_id, Post.created_at).filter(
            ~Post.user_id.in_(blocked_users),
            Post.user_id != user.id
        ).all()
        if not candidate_rows:
            return []

        candidate_ids = [pid for pid, _, _ in candidate_rows]
        post_created_map = {pid: created_at for pid, _, created_at in candidate_rows}

        post_tags: Dict[int, List[str]] = defaultdict(list)
        for pid, tname in (session.query(PostTag.post_id, Tag.tag_name)
                           .join(Tag, PostTag.tag_id == Tag.id)
                           .filter(PostTag.post_id.in_(candidate_ids)).all()):
            post_tags[pid].append(tname)

        state = self._get_user_state(user, session)
        top_tags = set(state["top_tags"])

        recent_view_tags = set()
        view_rows = (session.query(Tag.tag_name)
                     .join(PostTag, PostTag.tag_id == Tag.id)
                     .join(Action, Action.post_id == PostTag.post_id)
                     .filter(Action.user_id == user.id,
                             Action.action_type == 'view',
                             Action.timestamp > datetime.utcnow() - timedelta(days=1))
                     .all())
        for (t,) in view_rows:
            recent_view_tags.add(t)

        def avg_post_reward(pid: int) -> float:
            r = self._post_rewards.get(pid)
            return sum(r) / len(r) if r else 0.0

        def avg_tag_reward(tags: List[str]) -> float:
            if not tags:
                return 0.0
            vals = [sum(self._user_tag_rewards[user.id][t]) / len(self._user_tag_rewards[user.id][t])
                    for t in tags if t in self._user_tag_rewards[user.id]]
            if not vals:
                vals = [sum(self._tag_rewards[t]) / len(self._tag_rewards[t])
                        for t in tags if t in self._tag_rewards]
            return mean(vals) if vals else 0.0

        def combined_score(pid: int) -> float:
            # --- 基礎分數（保持你原本的計算） ---
            p_score = avg_post_reward(pid)
            t_score = avg_tag_reward(post_tags.get(pid, []))
            bonus = 0.0
            if set(post_tags[pid]) & top_tags:
                bonus += 0.2
            if set(post_tags[pid]) & recent_view_tags:
                bonus += 0.15

            # recency bonus（72 小時線性衰減，最高 +0.1）
            post_time = post_created_map[pid]
            age_hours = (datetime.utcnow() - post_time).total_seconds() / 3600
            bonus += max(0.0, (72 - age_hours) / 72) * 0.1

            score = (1 - self.tag_weight) * p_score + self.tag_weight * t_score + bonus

            # --- α 係數（階梯式） --------------------------------
            if pid in viewed_post_ids:               # 只有看過的才考慮折扣
                has_like    = pid in liked_post_ids
                has_comment = pid in commented_post_ids

                if has_like and has_comment:         # view + like + comment
                    α = 0.8                        # 幾乎不打折
                elif has_like:                       # view + like
                    α = 0.4                         # 輕微折扣
                else:                                # 只有 view
                    α = 0.3                         # 打 5 折
                score *= α                           # 套用係數

            # 沒 view ⇒ α = 1.0（不打折）
            return score
        
        k_main = int(k * (1 - explore_ratio))
        sorted_pref = sorted(candidate_ids, key=combined_score, reverse=True)

        main_ids = []
        for pid in sorted_pref:
            main_ids.append(pid)
            if len(main_ids) == k_main:
                break

        explore_pool = [pid for pid in candidate_ids
                        if pid not in viewed_post_ids and pid not in main_ids]
        random.shuffle(explore_pool)
        explore_ids = explore_pool[: k - len(main_ids)]

        return (main_ids + explore_ids)[:k]

    def _get_user_state(self, user, session) -> Dict:
        cutoff = datetime.utcnow() - timedelta(days=7)
        recent = (session.query(Action.action_type, Action.timestamp, Tag.tag_name)
                  .join(PostTag, PostTag.post_id == Action.post_id)
                  .join(Tag, PostTag.tag_id == Tag.id)
                  .filter(Action.user_id == user.id, Action.timestamp > cutoff)
                  .all())

        tag_counter = defaultdict(int)
        for _, _, tag in recent:
            tag_counter[tag] += 1

        last_active = max([ts for _, ts, _ in recent], default=datetime.utcnow())
        return {
            "top_tags": sorted(tag_counter, key=tag_counter.get, reverse=True)[:5],
            "last_active_minutes": (datetime.utcnow() - last_active).seconds // 60
        }


bandit_recommender = TagAwareBandit()
