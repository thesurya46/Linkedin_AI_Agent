import sqlite3
import modules
from modules.memory import get_average_engagement
from modules.memory import get_topic_engagement_score
from modules.topic_generator import generate_new_topics 
from difflib import SequenceMatcher

DB_PATH = "database/posts.db"


TOPIC_POOL = [
    {"name": "AI vs Automation in modern systems", "relevance": 0.9, "trend": 0.8},
    {"name": "Why consistency beats motivation", "relevance": 0.7, "trend": 0.6},
    {"name": "The rise of AI agents in 2025", "relevance": 0.95, "trend": 0.9},
    {"name": "Building in public as a developer", "relevance": 0.8, "trend": 0.7},
    {"name": "Why most automation projects fail", "relevance": 0.85, "trend": 0.75},
    {"name": "Prompt engineering vs system design", "relevance": 0.88, "trend": 0.82}
]


def init_db_if_needed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (topic TEXT)")
    conn.commit()
    conn.close()


def get_used_topics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT topic FROM posts")
    used = {row[0] for row in cursor.fetchall()}
    conn.close()
    return used


def score_topic(topic):
    base_score = 0.6 * topic["relevance"] + 0.4 * topic["trend"]

    performance_score = get_topic_engagement_score(topic["name"])

    adaptive_multiplier = 1 + performance_score

    return base_score * adaptive_multiplier
def get_next_topic():
    used_topics = get_used_topics()

    available_topics = [
        topic for topic in TOPIC_POOL
        if topic["name"] not in used_topics
    ]

    
    if not available_topics:
        print("⚡ Topic pool exhausted. Generating new topics...")
    new_topics = modules.topic_generator.generate_new_topics()

    for t in new_topics:
        if not is_similar_to_existing(t):
            TOPIC_POOL.append({
                "name": t,
                "relevance": 0.8,
                "trend": 0.8
            })
        else:
            print(f"⚠ Skipped similar topic: {t}")

    available_topics = [
        topic for topic in TOPIC_POOL
        if topic["name"] not in used_topics
    ]# Score and select highest
    best_topic = max(available_topics, key=score_topic)

    return best_topic["name"]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def is_similar_to_existing(new_topic: str, threshold: float = 0.7) -> bool:
    for topic in TOPIC_POOL:
        if similarity(new_topic, topic["name"]) > threshold:
            return True
    return False