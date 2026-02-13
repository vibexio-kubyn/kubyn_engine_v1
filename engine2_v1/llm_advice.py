import pymysql
import logging
from openai import OpenAI
from google import genai

from config import (
    DEEPSEEK_CONFIG,
    OPENAI_CONFIG,
    GEMINI_CONFIG,
    MYSQL_CONFIG
)

logger = logging.getLogger("engine2-llm")

# OpenAI client
openai_client = OpenAI(
    api_key=OPENAI_CONFIG["api_key"]
)

# DeepSeek client (OpenAI-compatible API)
deepseek_client = OpenAI(
    api_key=DEEPSEEK_CONFIG["api_key"],
    base_url="https://api.deepseek.com"
)

# Gemini client
gemini_client = genai.Client(
    api_key=GEMINI_CONFIG["api_key"]
)

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

def deepseek_generate(prompt):
    try:
        response = deepseek_client.chat.completions.create(
            model=DEEPSEEK_CONFIG["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=DEEPSEEK_CONFIG["temperature"],
            max_tokens=DEEPSEEK_CONFIG["max_tokens"]
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"DeepSeek failed | {str(e)}")


def openai_generate(prompt):
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_CONFIG["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=OPENAI_CONFIG["temperature"],
            max_tokens=OPENAI_CONFIG["max_tokens"]
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"OpenAI failed | {str(e)}")


def gemini_generate(prompt):
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_CONFIG["model"],
            contents=prompt,
            config={
                "temperature": GEMINI_CONFIG["temperature"],
                "max_output_tokens": GEMINI_CONFIG["max_tokens"]
            }
        )

        if not response.text:
            raise Exception("Empty Gemini response")

        return response.text

    except Exception as e:
        raise Exception(f"Gemini failed | {str(e)}")


def llm_generate(prompt):
    """
    Failover order:
    1. DeepSeek
    2. OpenAI
    3. Gemini

    Returns first successful response.
    Never exposes provider failures.
    """

    # 1️⃣ DeepSeek
    try:
        result = deepseek_generate(prompt)
        logger.info("LLM success | provider=DeepSeek")
        return result
    except Exception as e:
        logger.error(f"LLM failure | provider=DeepSeek | error={e}")

    # 2️⃣ OpenAI
    try:
        result = openai_generate(prompt)
        logger.info("LLM success | provider=OpenAI")
        return result
    except Exception as e:
        logger.error(f"LLM failure | provider=OpenAI | error={e}")

    # 3️⃣ Gemini
    try:
        result = gemini_generate(prompt)
        logger.info("LLM success | provider=Gemini")
        return result
    except Exception as e:
        logger.error(f"LLM failure | provider=Gemini | error={e}")

    logger.critical("All LLM providers failed")

    return "AI service temporarily unavailable. Please try again shortly."

def generate_llm_suggestion(user_id, expense_summary, goal_summary):
    engine1 = fetch_engine1_scores(user_id)

    prompt = f"""
ou are a behavioral finance intelligence system. 
Your task is to generate personalized, psychologically aligned financial guidance. 
You must NOT provide generic advice. You must NOT use fear, urgency, or pressure-based language. 
----------------------------- USER PSYCHOLOGICAL PROFILE (ENGINE 1) ----------------------------- 
Confidence Score: {engine1['confidence_score']} (0–100)
 Income–Expense Discipline Score: {engine1['income_expense_score']} 
 (0–100) Personality Type: {engine1['personality_type']}
   Financial Archetype: {engine1['archetype']} 
   ----------------------------- EXPENSE BEHAVIOUR ANALYSIS ----------------------------- 
   {expense_summary} 
   ----------------------------- GOAL & SURPLUS SIMULATION -----------------------------
     {goal_summary} ----------------------------- OUTPUT REQUIREMENTS ----------------------------- 
     1. Start with calm behavioral observation 
     2. Reference ONE spending pattern 
     3. Reference ONE goal-related action 
     4. Align with archetype 
     5. End with confidence-preserving close 
    Your response MUST NOT - 
    Mention "AI", 
    "model", or "algorithm" - 
    Give investment tips - 
    Suggest financial products - 
    Use absolute words like "always", "never", "must" Tone: Human, grounded, supportive.
    Generate final response now. """

    return llm_generate(prompt)
