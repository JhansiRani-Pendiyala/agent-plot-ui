from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import load_all_schema_contexts, QueryRequest
from app.database import init_db_pool, close_db_pool, run_query
from app.llm import generate_sql_query
from pathlib import Path
import logging
import json

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_PATH = Path(__file__).parent.parent / "config.json"
try:
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    logger.info("Loaded config.json")
except Exception as e:
    logger.error(f"Failed to load config.json: {e}")
    raise

@app.on_event("startup")
def startup():
    init_db_pool(config)

@app.on_event("shutdown")
def shutdown():
    close_db_pool()

@app.post("/api/query")
def query_handler(request: QueryRequest):
    user_prompt = request.query
    logger.info(f"Received query: {user_prompt}")

    schema_context = load_all_schema_contexts()
    sql_query = generate_sql_query(user_prompt, schema_context, config["OPENAI_API_KEY"])
    logger.info(f"Generated SQL: {sql_query}")

    if not sql_query.lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT statements are allowed.")

    try:
        columns, rows = run_query(sql_query)
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.exception("Query execution failed.")
        raise HTTPException(status_code=400, detail=str(e))