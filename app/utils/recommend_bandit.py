from __future__ import annotations

import re
from collections import defaultdict
from statistics import mean
from typing import Dict, List, Set
from datetime import datetime, timedelta

from app.models.model import db
from app.models.Action import Action
from app.models.Tag import Tag
from app.models.PostTag import PostTag
from app.models.Block import Block
from app.models.Comment import Comment
from app.models.Follow import Follow

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
        for post_id, tag_name in (
            session.query(PostTag.post_id, Tag.tag_name)
            .join(Tag, PostTag.tag_id == Tag.id)
            .all()
        ):
            post_tags[post_id].append(tag_name)

        cutoff = datetime.utcnow() - timedelta(days=30)

        for user_id, post_id, action_type, ts in (
            session.query(Action.user_id, Action.post_id, Action.action_type, Action.timestamp)
            .filter(Action.timestamp > cutoff)
            .all()
        ):
            if post_id is None:
                continue

            reward = REWARD_MAPPING.get(action_type, 0.0)
            age_days = (datetime.utcnow() - ts).days
            decay = 0.95 ** age_days
            weighted_reward = reward * decay

            self._post_rewards[post_id].append(weighted_reward)

            for tag_name in post_tags.get(post_id, []):
                self._tag_rewards[tag_name].append(weighted_reward)
                self._user_tag_rewards[user_id][tag_name].append(weighted_reward)

    def recommend_all(self, user, session, k=15) -> List[int]:
        from app.models.Post import Post

        cutoff = datetime.utcnow() - timedelta(days=30)
        viewed_post_ids = {
            pid for pid, in session.query(Action.post_id)
            .filter(
                Action.user_id == user.id,
                Action.action_type == 'view',
                Action.timestamp > cutoff
            )
        }

        state = self._get_user_state(user, session)

        blocked_users = {
            b.blocked_id for b in user.blocking.all()
        } | {
            b.blocker_id for b in user.blocked_by.all()
        }

        candidate_rows = (
            session.query(Post.id, Post.user_id)
            .filter(
                ~Post.user_id.in_(blocked_users),
                Post.user_id != user.id
            )
            .all()
        )
        if not candidate_rows:
            return []

        candidate_ids = [pid for pid, _ in candidate_rows]

        followee_ids = {
            f.followee_id
            for f in session.query(Follow).filter(Follow.follower_id == user.id).all()
        }
        followee_post_ids = [pid for pid, uid in candidate_rows if uid in followee_ids]
        commented_ids = {
            pid for pid, in session.query(Comment.post_id).filter(Comment.user_id.in_(followee_ids)).all()
        }
        priority_post_ids = set(followee_post_ids) | commented_ids

        post_to_tags: Dict[int, List[str]] = defaultdict(list)
        for pid, tag_name in (
            session.query(PostTag.post_id, Tag.tag_name)
            .join(Tag, PostTag.tag_id == Tag.id)
            .filter(PostTag.post_id.in_(candidate_ids))
            .all()
        ):
            post_to_tags[pid].append(tag_name)

        def avg_post_reward(pid: int) -> float:
            r = self._post_rewards.get(pid)
            return sum(r) / len(r) if r else 0.0

        def avg_tag_reward(tags: List[str], user_id: int) -> float:
            user_tags = self._user_tag_rewards.get(user_id, {})

            vals = [
                sum(user_tags[t]) / len(user_tags[t])
                for t in tags if t in user_tags and len(user_tags[t]) > 1
            ]
            if not vals:
                vals = [
                    sum(self._tag_rewards[t]) / len(self._tag_rewards[t])
                    for t in tags if t in self._tag_rewards and len(self._tag_rewards[t]) > 1
                ]
            return mean(vals) if vals else 0.0

        def combined_score(pid: int) -> float:
            p_score = avg_post_reward(pid)
            t_score = avg_tag_reward(post_to_tags.get(pid, []), user.id)
            bonus = 0.5 if pid in priority_post_ids else 0.0

            if pid in self._post_rewards:
                bonus += 0.3

            # ✅ 狀態轉移：使用者偏好 tag 被命中，加分
            post_tags = set(post_to_tags.get(pid, []))
            if post_tags & set(state["top_tags"]):
                bonus += 0.2

            score = (1 - self.tag_weight) * p_score + self.tag_weight * t_score + bonus

            # ✅ 若已看過則打折
            if pid in viewed_post_ids:
                score *= 0.3

            return score

        sorted_ids = sorted(candidate_ids, key=combined_score, reverse=True)
        return sorted_ids[:k]

    def _get_user_state(self, user, session) -> Dict:
        cutoff = datetime.utcnow() - timedelta(days=7)

        recent = session.query(
            Action.action_type,
            Action.timestamp,
            Tag.tag_name
        ).join(PostTag, PostTag.post_id == Action.post_id) \
         .join(Tag, PostTag.tag_id == Tag.id) \
         .filter(Action.user_id == user.id, Action.timestamp > cutoff).all()

        tag_counter = defaultdict(int)
        for action_type, ts, tag in recent:
            tag_counter[tag] += 1

        last_active = max([ts for _, ts, _ in recent], default=datetime.utcnow())

        return {
            "top_tags": sorted(tag_counter, key=tag_counter.get, reverse=True)[:5],
            "last_active_minutes": (datetime.utcnow() - last_active).seconds // 60
        }


bandit_recommender = TagAwareBandit()
