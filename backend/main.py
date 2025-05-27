import json
import psycopg2
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config from JSON file
CONFIG_PATH = Path(__file__).parent / "config.json"
try:
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    logger.info("Loaded config.json successfully")
except Exception as e:
    logger.error(f"Failed to load config.json: {e}")
    raise

OPENAI_API_KEY = config.get("OPENAI_API_KEY")

DB_HOST = config.get("DB_HOST", "localhost")
DB_PORT = config.get("DB_PORT", "5432")
DB_NAME = config.get("DB_NAME", "yourdb")
DB_USER = config.get("DB_USER", "youruser")
DB_PASSWORD = config.get("DB_PASSWORD", "yourpassword")

SCHEMA_DIR = Path(__file__).parent / "schemas"

class QueryRequest(BaseModel):
    query: str

def extract_sql_query(llm_response: str) -> str:
    if not llm_response:
        return ""
    start = llm_response.find("```sql")
    if start != -1:
        end = llm_response.find("```", start + 6)
        if end != -1:
            return llm_response[start+6:end].strip()
    return llm_response.strip()

def load_all_schema_contexts() -> str:
    schema_files = SCHEMA_DIR.glob("*.txt")
    contexts = []
    for file in schema_files:
        try:
            content = file.read_text(encoding="utf-8").strip()
            logger.debug(f"Loaded schema file: {file.name}")
            contexts.append(content)
        except Exception as e:
            logger.error(f"Error reading schema file {file.name}: {e}")
    combined = "\n\n".join(contexts)
    logger.info(f"Loaded {len(contexts)} schema files.")
    return combined

@app.post("/api/query")
def generate_and_execute(request: QueryRequest):
    user_prompt = request.query
    logger.info(f"Received query: {user_prompt}")

    schema_context = load_all_schema_contexts()

    system_prompt = (
        "You are a helpful assistant that generates one valid PostgreSQL SQL query  based on best match"
        "based on the schema and user request. " + schema_context
    )

    full_prompt = f"Generate a single SQL query for this request: {user_prompt}"

    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0,
        "n": 1,
        "max_tokens": 500,
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    logger.debug("Sending request to OpenAI API.")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code != 200:
        logger.error(f"OpenAI API error: {response.text}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {response.text}")

    body = response.json()
    sql_query = extract_sql_query(body["choices"][0]["message"]["content"])
    logger.info(f"Generated SQL based on User input: {sql_query}")

    if not sql_query.lower().startswith("select"):
        logger.warning("Generated SQL is not a SELECT statement.")
        raise HTTPException(status_code=400, detail="Generated SQL is not a SELECT statement.")

    try:
        logger.debug("Connecting to PostgreSQL database.")
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        logger.debug("Executing SQL query on database.")
        cur.execute(sql_query)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall() if cur.description else []
        cur.close()
        conn.close()
        logger.info(f"Query executed successfully. Rows returned: {len(rows)}")

        results = []
        for row in rows:
            row_dict = {}
            for col, val in zip(columns, row):
                row_dict[col] = list(val) if isinstance(val, (list, tuple)) else val
            results.append(row_dict)

        return results

    except Exception as e:
        logger.exception("Database query failed.")
        raise HTTPException(status_code=400, detail=str(e))
