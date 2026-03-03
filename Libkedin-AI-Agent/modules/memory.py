import sqlite3
from datetime import datetime

DB_PATH = "database/posts.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE,
            content TEXT,
            created_at TEXT,
            posting_hour INTEGER,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            impressions INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def topic_exists(topic: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM posts WHERE topic = ?", (topic,))
    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_post(topic: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.utcnow()
    posting_hour = now.hour

    cursor.execute("""
        INSERT INTO posts (
            topic,
            content,
            created_at,
            posting_hour,
            likes,
            comments,
            impressions
        )
        VALUES (?, ?, ?, ?, 0, 0, 0)
    """, (
        topic,
        content,
        now.isoformat(),
        posting_hour
    ))

    conn.commit()
    conn.close()

def update_engagement(topic: str, likes: int, comments: int, impressions: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE posts
        SET likes = ?, comments = ?, impressions = ?
        WHERE topic = ?
    """, (likes, comments, impressions, topic))

    conn.commit()
    conn.close()

def calculate_engagement_score(likes: int, comments: int, impressions: int) -> float:
    if impressions == 0:
        return 0.0

    return (0.4 * likes + 0.6 * comments) / impressions

def get_average_engagement():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT likes, comments, impressions FROM posts
        WHERE impressions > 0
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0.0

    scores = [
        calculate_engagement_score(l, c, i)
        for l, c, i in rows
    ]

    return sum(scores) / len(scores)

def get_topic_engagement_score(topic: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT likes, comments, impressions
        FROM posts
        WHERE topic = ? AND impressions > 0
    """, (topic,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0.0

    scores = [
        calculate_engagement_score(l, c, i)
        for l, c, i in rows
    ]

    return sum(scores) / len(scores)

def get_best_posting_hour():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT posting_hour, likes, comments, impressions
        FROM posts
        WHERE impressions > 0
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 9  

    hour_scores = {}

    for hour, likes, comments, impressions in rows:
        score = calculate_engagement_score(likes, comments, impressions)
        if hour not in hour_scores:
            hour_scores[hour] = []
        hour_scores[hour].append(score)

    avg_scores = {
        hour: sum(scores)/len(scores)
        for hour, scores in hour_scores.items()
    }

    return max(avg_scores, key=avg_scores.get)

def get_top_performing_post():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content, likes, comments, impressions
        FROM posts
        WHERE impressions > 0
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    best = max(
        rows,
        key=lambda r: calculate_engagement_score(r[1], r[2], r[3])
    )

    return best[0]