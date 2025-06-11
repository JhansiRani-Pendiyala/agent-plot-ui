import requests
import logging

logger = logging.getLogger(__name__)

def extract_sql_query(llm_response: str) -> str:
    if not llm_response:
        return ""
    start = llm_response.find("```sql")
    if start != -1:
        end = llm_response.find("```", start + 6)
        if end != -1:
            return llm_response[start+6:end].strip()
    return llm_response.strip()

def generate_sql_query(prompt: str, schema_context: str, api_key: str) -> str:
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant... {schema_context}"},
            {"role": "user", "content": f"Generate a single SQL query for this request: {prompt}"}
        ],
        "temperature": 0,
        "n": 1,
        "max_tokens": 500,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"OpenAI API request failed: {e}")
        raise

    body = response.json()
    return extract_sql_query(body["choices"][0]["message"]["content"])
