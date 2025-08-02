# agents/llm_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama3-70b-8192"  # or "llama3-70b-8192"

def suggest_improvements(file_content: str, file_type: str) -> str:
    system_prompt = f"You are an expert DevOps reviewer. Analyze this {file_type} and suggest improvements in security, maintainability, or DevOps hygiene."
    user_input = f"{file_type} Content:\n{file_content}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
