from pathlib import Path
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)
SCHEMA_DIR = Path(__file__).parent.parent / "schemas"

def load_all_schema_contexts() -> str:
    schema_files = SCHEMA_DIR.glob("*.txt")
    contexts = []
    for file in schema_files:
        try:
            contexts.append(file.read_text(encoding="utf-8").strip())
            logger.debug(f"Loaded schema file: {file.name}")
        except Exception as e:
            logger.error(f"Error reading schema file {file.name}: {e}")
    logger.info(f"Loaded {len(contexts)} schema files.")
    return "\n\n".join(contexts)

class QueryRequest(BaseModel):
    query: str