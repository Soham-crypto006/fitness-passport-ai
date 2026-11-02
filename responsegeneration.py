
import os
from google import genai

def build_prompt(user_question, retrieved_chunks):
    prompt = "Answer the user's question using ONLY the provided context below.\n\nContext:\n---\n"

    for chunk in retrieved_chunks:
        prompt += f"{chunk}\n---\n"

    prompt += f"\nUser Question: {user_question}\n"
    return prompt


def get_ollama_response(prompt, retrieved_metadatas, model_name="gemini-2.5-flash"):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    text = response.text + "\n\n**References:**\n"

    for source in set([meta["source"] for meta in retrieved_metadatas]):
        text += f"- [{source}]({source})\n"

    return text
