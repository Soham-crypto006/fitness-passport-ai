import ollama

def build_prompt(user_question, retrieved_chunks):
    prompt = "Answer the user's question using ONLY the provided context below.\n\nContext:\n---\n"
    for chunk in retrieved_chunks:
        prompt += f"{chunk}\n---\n"
    prompt += f"\nUser Question: {user_question}\n"
    return prompt

def get_ollama_response(prompt, retrieved_metadatas, model_name="llama3.2"):
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    text = response['message']['content'] + "\n\n**References:**\n"
    
    for source in set([meta["source"] for meta in retrieved_metadatas]):
        text += f"- [{source}]({source})\n"
    return text