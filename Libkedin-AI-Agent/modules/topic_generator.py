from modules.generator import generate_post


def generate_new_topics():
    prompt = """
    Generate 5 high-quality LinkedIn post topics
    related to AI, automation, productivity,
    system design, or developer growth.
    
    Return them as a simple numbered list.
    """

    response = generate_post(prompt)

    topics = []

    for line in response.split("\n"):
        if line.strip() and line[0].isdigit():
            topic = line.split(".", 1)[-1].strip()
            topics.append(topic)

    return topics