from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('AI_API_URL')
)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                 }
            ],
            temperature=0.7,
            max_tokens=10000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"


def get_detailed_prompt_by_ai(prompt) -> str:
    detailed_prompt = f""" ... {prompt} ... """
    response = ask_ai(detailed_prompt)

    if response is None:
        return "Car"

    return response
