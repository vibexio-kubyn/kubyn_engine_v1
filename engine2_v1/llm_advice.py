import logging
import pymysql
from openai import OpenAI
from config import DB_CONFIG, OPENROUTER_API_KEY, MODEL_PRIORITY, TEMPERATURE, MAX_TOKENS

# -------------------- LOGGING --------------------
logging.basicConfig(
    filename="kubyn_ai.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("Kubyn-AI")

# -------------------- OPENROUTER CLIENT --------------------
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Kubyn AI Engine"
    }
)

# ============================================================
# ENGINE 1 DATA FETCH
# ============================================================

def fetch_engine1_scores(user_id):
    """Fetch behavioral finance psychology scores"""

    try:
        conn = pymysql.connect(
            **DB_CONFIG,
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT confidence_score,
                       income_score,
                       expense_score,
                       savings_score,
                       archetype,
                       personality_type
                FROM engine1_scores
                WHERE user_id = %s
                ORDER BY run_timestamp DESC
                LIMIT 1
            """, (user_id,))

            row = cursor.fetchone()

        conn.close()

        if not row:
            raise ValueError("No engine1 record")

        return {
            "confidence_score": row["confidence_score"],
            "income_score": row["income_score"],
            "expense_score": row["expense_score"],
            "savings_score": row["savings_score"],
            "income_expense_score": (row["income_score"] + row["expense_score"]) // 2,
            "personality_type": row["personality_type"],
            "archetype": row["archetype"]
        }

    except Exception as e:
        logger.warning(f"Engine1 fallback used | user_id={user_id} | {e}")

        return {
            "confidence_score": 50,
            "income_score": 50,
            "expense_score": 50,
            "savings_score": 50,
            "income_expense_score": 50,
            "personality_type": "Adventurer",
            "archetype": "Safety Netter"
        }

# ============================================================
# LLM ROUTER (Priority Fallback)
# ============================================================

def generate_llm_text(prompt: str):

    last_error = None

    for model in MODEL_PRIORITY:
        if not model:
            continue

        try:
            logger.info(f"Trying model: {model}")

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                timeout=45
            )

            text = response.choices[0].message.content

            if not text:
                raise ValueError("Empty response from model")

            logger.info(f"Model success: {model}")

            return text.strip()

        except Exception as e:
            logger.error(f"{model} failed | {e}")
            last_error = str(e)
            continue

    logger.critical(f"All models failed | Last error: {last_error}")

    return (
        "I couldn’t generate a personalized reflection right now. "
        "Your patterns are still being understood — please try again shortly."
    )

# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(engine1, expense_summary, goal_summary):

    return f"""
You are a behavioral finance psychologist.

You generate personalized financial guidance aligned to the user's psychology.

Rules:
- No generic advice
- No investments
- No products
- No pressure language
- No mentioning AI or model

---------------- USER PSYCHOLOGICAL PROFILE ----------------
Confidence Score: {engine1['confidence_score']} (0–100)
Income–Expense Discipline Score: {engine1['income_expense_score']} (0–100)
Personality Type: {engine1['personality_type']}
Financial Archetype: {engine1['archetype']}

---------------- EXPENSE BEHAVIOUR ANALYSIS ----------------
{expense_summary}

---------------- GOAL & SURPLUS SIMULATION ----------------
{goal_summary}

---------------- OUTPUT REQUIREMENTS ----------------
1. Start with calm behavioral observation
2. Reference ONE spending pattern
3. Reference ONE goal-related action
4. Align with archetype
5. End with confidence-preserving close

Do not mention AI, model, or algorithm.
Do not suggest investments or financial products.
Avoid absolute words like always, never, must.

Generate the final response now.
"""

# ============================================================
# PUBLIC FUNCTION (THIS IS WHAT YOUR API CALLS)
# ============================================================

def generate_llm_suggestion(user_id, expense_summary, goal_summary):

    engine1 = fetch_engine1_scores(user_id)

    prompt = build_prompt(engine1, expense_summary, goal_summary)

    recommendation = generate_llm_text(prompt)

    return recommendation
