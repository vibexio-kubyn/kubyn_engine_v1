import requests
import pymysql
from config import DEEPSEEK_CONFIG

def fetch_engine1_scores(user_id):
    """Fetch Engine 1 scores from database using pymysql"""
    try:
        conn = pymysql.connect(
            host="localhost",
            user="kubyn",
            password="Venkat@3929",
            database="kubyn",
            port=3306
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT confidence_score, income_score, expense_score, savings_score, 
                       archetype, personality_type 
                FROM engine1_scores 
                WHERE user_id = %s 
                ORDER BY run_timestamp DESC 
                LIMIT 1
            """, (user_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                confidence_score, income_score, expense_score, savings_score, archetype, personality_type = row
                # Calculate income_expense_score as average of income and expense scores
                income_expense_score = (income_score + expense_score) // 2
                
                return {
                    "confidence_score": confidence_score,
                    "income_score": income_score,
                    "expense_score": expense_score,
                    "savings_score": savings_score,
                    "income_expense_score": income_expense_score,
                    "personality_type": personality_type,
                    "archetype": archetype
                }
            else:
                # Return default scores if not found
                return {
                    "confidence_score": 50,
                    "income_score": 50,
                    "expense_score": 50,
                    "savings_score": 50,
                    "income_expense_score": 50,
                    "personality_type": "Adventurer",
                    "archetype": "Safety Netter"
                }
                
    except Exception as e:
        print(f"Error fetching engine1 scores: {e}")
        # Return default scores on error
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
    """Generate response using DeepSeek API"""
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_CONFIG['api_key']}",
                "Content-Type": "application/json"
            },
            json={
                "model": DEEPSEEK_CONFIG["model"],
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": DEEPSEEK_CONFIG["temperature"],
                "max_tokens": DEEPSEEK_CONFIG["max_tokens"]
            },
            timeout=30
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"DeepSeek API error: {e}")
        # Return fallback response
        return """I notice you're reviewing your financial patterns. Let's focus on one spending area that could be adjusted slightly. 
Based on your goals, consider allocating a small portion of any surplus to build momentum. 
Remember, consistent small steps lead to meaningful progress over time."""

def generate_llm_suggestion(user_id, expense_summary, goal_summary):
    """Generate personalized financial advice"""
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
1. Start with a calm behavioral observation (1–2 lines)
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

    recommendation = deepseek_generate(prompt)
    return recommendation
