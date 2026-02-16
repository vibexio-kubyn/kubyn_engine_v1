import os
from dotenv import load_dotenv
from pathlib import Path

# Find the folder where THIS config.py exists
CURRENT_DIR = Path(__file__).resolve().parent

# Look for .env in the SAME folder
ENV_FILE = CURRENT_DIR / ".env"

# Load it explicitly (no guessing)
load_dotenv(dotenv_path=ENV_FILE)

# Now read variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        f"OPENROUTER_API_KEY not found. Expected .env at: {ENV_FILE}"
    )

# Database
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# Model priority
MODEL_PRIORITY = [
    os.getenv("PRIMARY_MODEL"),
    os.getenv("SECONDARY_MODEL"),
    os.getenv("BACKUP_MODEL")
]

MODEL_PRIORITY = [m for m in MODEL_PRIORITY if m]
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.6))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 700))