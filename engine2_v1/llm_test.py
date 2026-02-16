"""
Test OpenRouter model fallback
Run: python test_claude.py
"""

import logging
from openai import OpenAI
from config import OPENROUTER_API_KEY, MODEL_PRIORITY, TEMPERATURE, MAX_TOKENS

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("model-test")

# ---------------- CLIENT ----------------
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Kubyn AI Engine"
    }
)

# ---------------- PROMPT ----------------
prompt = """
You are a behavioral finance psychologist.

You generate personalized financial guidance aligned to the user's psychology.

Rules:
- No generic advice
- No investments
- No products
- No pressure language
- No mentioning AI or model

---------------- USER PSYCHOLOGICAL PROFILE ----------------
Confidence Score: 26 (0–100)
Income–Expense Discipline Score: 72.5 (0–100)
Personality Type: hedonist
Financial Archetype: {Rag to riches}

---------------- EXPENSE BEHAVIOUR ANALYSIS ----------------
"period_days": 7, "total_spent": 67000.0, "breakdown": [{"category": "Rent", "amount": 8000.0, "share": 0.12, "status": "healthy"}, {"category": "Travel", "amount": 9000.0, "share": 0.13, "status": "healthy"}

---------------- GOAL & SURPLUS SIMULATION ----------------
{"surplus": 3000.0, "suggested_allocations": [{"goal_id": 66, "suggested_amount": 2000.0}, {"goal_id": 67, "suggested_amount": 1000.0}], "remaining_unallocated": 0.0}

---------------- OUTPUT REQUIREMENTS ----------------
1. Start with calm behavioral observation
2. Reference ONE spending pattern
3. Reference ONE goal-related action
4. Align with archetype
5. End with confidence-preserving close
8.Not complicated, keep it simple and concise.

Do not mention AI, model, or algorithm.
Do not suggest investments or financial products.
Avoid absolute words like always, never, must.

Generate the final response now .
"""

def test_models():
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

            if not text or text.strip() == "":
                raise ValueError("Empty response from model")

            logger.info(f"SUCCESS from {model}\n")

            print("\n================ RESPONSE ================\n")
            print(text.strip())
            print("\n==========================================\n")

            return

        except Exception as e:
            logger.error(f"{model} failed | {e}")
            last_error = str(e)
            continue

    logger.critical(f"All models failed | Last error: {last_error}")
    print("All models failed. Check API key or credits.")


# ---------------- RUN ----------------
if __name__ == "__main__":
    test_models()
