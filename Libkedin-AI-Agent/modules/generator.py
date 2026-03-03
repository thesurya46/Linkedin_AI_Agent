from openai import OpenAI
from config import OPENROUTER_API_KEY
from modules.memory import get_top_performing_post

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def generate_post(topic: str) -> str:
    top_post = get_top_performing_post()

    tone_instruction = ""

    if top_post:
        tone_instruction = """
        Analyze the structure and tone of the previously high-performing post.
        Mimic its writing style (hook strength, structure, pacing),
        but DO NOT copy content.
        """

    system_prompt = f"""
    You are a LinkedIn content strategist.

    Write engaging, high-quality LinkedIn posts that:
    - Start with a strong hook
    - Are easy to read (short paragraphs)
    - Provide insight or value
    - End with a thought-provoking close

    {tone_instruction}
    """

    user_prompt = f"""
    Write a LinkedIn post about:
    {topic}
    """

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content