from modules.generator import generate_post
from modules.memory import init_db, save_post
from modules.topic_manager import get_next_topic
from modules.publisher import publish_post


def run_workflow():
    print("🚀 Starting workflow...")

    init_db()

    topic = get_next_topic()

    if not topic:
        print("No topic available.")
        return

    print(f"🧠 Selected topic: {topic}")

    post = generate_post(topic)

    print("✍ Generated post:")
    print(post)

    save_post(topic, post)

    print("💾 Post saved to database.")

    status, response = publish_post(post)

    if status == 201:
        print("🚀 Successfully published to LinkedIn!")
    else:
        print(f"❌ Publishing failed: {status}")
        print(response)