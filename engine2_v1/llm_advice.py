import requests
import pymysql
import logging
from config import DEEPSEEK_CONFIG, MYSQL_CONFIG

logger = logging.getLogger("engine2-llm")

# Fetch Engine 1 scores
def fetch_engine1_scores(user_id):
    try:
        conn = pymysql.connect(
            **MYSQL_CONFIG,
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
            raise ValueError("No Engine-1 data found")

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
        logger.warning(f"Using default Engine-1 scores | user_id={user_id} | {e}")
        return {
            "confidence_score": 50,
            "income_score": 50,
            "expense_score": 50,
            "savings_score": 50,
            "income_expense_score": 50,
            "personality_type": "Adventurer",
            "archetype": "Safety Netter"
        }

# DeepSeek LLM call
def deepseek_generate(prompt):
    """
    Generate response using DeepSeek LLM.
    """
    try:
        response = requests.post(
            DEEPSEEK_CONFIG["url"],
            headers={
                "Authorization": f"Bearer {DEEPSEEK_CONFIG['api_key']}",
                "Content-Type": "application/json"
            },
            json={
                "model": DEEPSEEK_CONFIG["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": DEEPSEEK_CONFIG["temperature"],
                "max_tokens": DEEPSEEK_CONFIG["max_tokens"]
            },
            timeout=30
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        logger.error(f"DeepSeek API failed | {e}")
        return (
            "I notice you're reflecting on your financial patterns. "
            "Small, steady adjustments can make progress feel more natural. "
            "You're building awareness, and that matters."
        )

# Main advice generator (FULL PROMPT)
def generate_llm_suggestion(user_id, expense_summary, goal_summary):
    """
    Generate personalized, psychologically aligned financial advice.
    """
    engine1 = fetch_engine1_scores(user_id)

    prompt = f"""
You are a behavioral finance intelligence system.

Your task is to generate personalized, psychologically aligned financial guidance.
You must NOT provide generic advice.
You must NOT use fear, urgency, or pressure-based language.

-----------------------------
USER PSYCHOLOGICAL PROFILE (ENGINE 1)
-----------------------------
Confidence Score: {engine1['confidence_score']} (0–100)
Income–Expense Discipline Score: {engine1['income_expense_score']} (0–100)
Personality Type: {engine1['personality_type']}
Financial Archetype: {engine1['archetype']}

Interpretation Rules:
- Low confidence → reassurance, small steps
- High confidence → structured, autonomy-respecting advice
- Archetype defines long-term vs short-term framing
- Personality defines tone and motivation style

-----------------------------
EXPENSE BEHAVIOUR ANALYSIS
-----------------------------
{expense_summary}

Interpretation Rules:
- Identify overspending categories
- Do NOT shame the user
- Reframe spending as behavior patterns, not mistakes
- Suggest adjustment ranges, not hard cuts

-----------------------------
GOAL & SURPLUS SIMULATION
-----------------------------
{goal_summary}

Interpretation Rules:
- Explain why surplus allocation matters psychologically
- Reinforce consistency over speed
- If surplus exists, frame it as optional empowerment
- If no surplus, normalize and stabilize behavior

-----------------------------
OUTPUT REQUIREMENTS
-----------------------------
Your response MUST:
1. Start with a calm behavioral observation (1-2 lines)
2. Reference ONE spending pattern (not all)
3. Reference ONE goal-related action
4. Align advice with the user's archetype
5. End with a confidence-preserving closing statement

Your response MUST NOT:
- Mention "AI", "model", or "algorithm"
- Give investment tips
- Suggest financial products
- Use absolute words like "always", "never", "must"

Tone:
- Human
- Grounded
- Supportive
- Non-judgmental

Generate the final response now.
"""

    return deepseek_generate(prompt)
