import os
import sys
import logging
from datetime import datetime
import pymysql

# Add parent dir to path if running directly
print("DEBUG: Initializing Engine 1...", flush=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from confidence import calculate_confidence
from income_expense import calculate_income_expense
from archetype import determine_archetype
from personality import determine_personality
logger = logging.getLogger(__name__)


# ENUM NORMALIZATION MAPS

ARCHETYPE_ENUM = {
    "rag to riches": "Rag to Riches",
    "safety netter": "Safety Netter",
    "trend rider": "Trend Rider",
    "freedom seeker": "Freedom Seeker",
    "big dreamer": "Big Dreamer",
    "legacy builder": "Legacy Builder"
}

PERSONALITY_ENUM = {
    "adventurer": "Adventurer",
    "hedonist": "Hedonist",
    "minimalist": "Minimalist",
    "creator": "Creator",
    "achiever": "Achiever",
    "caregiver": "Caregiver"
}

# Utility functions
def _normalize_enum(value: str, enum_map: dict, default: str) -> str:
    if not value:
        return default
    key = value.strip().lower()
    return enum_map.get(key, default)


def _clamp_score(value: float) -> int:
    return max(0, min(100, int(round(value))))

# Core Engine Logic

def process_engine_one(user_context: dict, answers: dict) -> dict:
    """
    Run Engine-1 computation for a single user.

    user_context MUST contain:
    {
        "id": <user_id>
    }
    """

    if not isinstance(user_context, dict) or "id" not in user_context:
        raise ValueError("user_context must be a dict containing 'id'")

    if not isinstance(answers, dict):
        raise ValueError("answers must be a dictionary")

    logger.info(f"Running Engine-1 computation for user {user_context['id']}")

    # Confidence
    confidence_score = calculate_confidence(user_context, answers)

    # Income & Expense
    ie = calculate_income_expense(answers)

    # Archetype & Personality
    archetype = determine_archetype(answers)
    personality = determine_personality(answers)

    return {
        "confidence_score": confidence_score,
        "income_score": ie.get("income_score", 0),
        "expense_score": ie.get("expense_score", 0),
        "savings_score": ie.get("savings_score", 0),
        "archetype": archetype,
        "personality": personality
    }

# Database Storage
def store_engine1_output(user_id: str, result: dict):
    """
    Persist Engine-1 output to database.
    Raises exception on failure (API layer decides response).
    """

    logger.info(f"Storing Engine-1 result for user {user_id}")

    archetype = _normalize_enum(
        result.get("archetype"),
        ARCHETYPE_ENUM,
        "Safety Netter"
    )

    personality = _normalize_enum(
        result.get("personality"),
        PERSONALITY_ENUM,
        "Adventurer"
    )

    params = (
        user_id,
        datetime.now(),
        _clamp_score(result.get("confidence_score", 0)),
        _clamp_score(result.get("income_score", 0)),
        _clamp_score(result.get("expense_score", 0)),
        _clamp_score(result.get("savings_score", 0)),
        archetype,
        personality,
        1  # engine_version
    )

    try:
        conn = pymysql.connect(
            host=os.getenv("localhost"),
            user=os.getenv("kubyn"),
            password=os.getenv("Venkat@3929"),
            database=os.getenv("kubyn"),
            port=3306,
            cursorclass=pymysql.cursors.Cursor
        )

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO engine1_scores
                (user_id, run_timestamp, confidence_score, income_score,
                 expense_score, savings_score, archetype,
                 personality_type, engine_version)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                run_timestamp=VALUES(run_timestamp),
                confidence_score=VALUES(confidence_score),
                income_score=VALUES(income_score),
                expense_score=VALUES(expense_score),
                savings_score=VALUES(savings_score),
                archetype=VALUES(archetype),
                personality_type=VALUES(personality_type),
                engine_version=VALUES(engine_version)
                """,
                params
            )

        conn.commit()
        conn.close()

        logger.info(f"Engine-1 output stored successfully for user {user_id}")

    except Exception:
        logger.exception(f"Failed to store Engine-1 output for user {user_id}")
        raise
