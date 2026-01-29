import sys
import os
from datetime import datetime
import pymysql

# Add parent dir to path if running directly
print("DEBUG: Initializing Engine 1...", flush=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from confidence import calculate_confidence
from income_expense import calculate_income_expense
from archetype import determine_archetype
from personality import determine_personality

print("DEBUG: Imports successful.", flush=True)

def process_engine_one(user_data, question_data):
    """
    Compute all four outputs for one user
    """
    # confidence expects (user, q) but ignores user.
    confidence_score = calculate_confidence(user_data, question_data)
    
    # income_expense takes q
    income_expense = calculate_income_expense(question_data)
    income_score = income_expense["income_score"]
    expense_score = income_expense["expense_score"]
    savings_score = income_expense["savings_score"]
    
    # archetype takes q
    archetype = determine_archetype(question_data)
    
    # personality takes q
    personality = determine_personality(question_data)
    
    return {
        "confidence_score": confidence_score,
        "income_score": income_score,
        "expense_score": expense_score,
        "savings_score": savings_score,
        "archetype": archetype,
        "personality": personality
    }

def map_to_db_enum(result):
    """Map engine output to valid database ENUM values"""
    # Map archetype
    archetype_map = {
        'Rag-to-Richess': 'Rag to Riches',
        'The Safety Netter': 'Safety Netter',
        'The Trend Rider': 'Trend Rider',
        'The Freedom Seeker': 'Freedom Seeker',
        'The Big Dreamer': 'Big Dreamer',
        'The Legacy Builder': 'Legacy Builder',
        'Rag-to-Riches': 'Rag to Riches',
        'Safety Netter': 'Safety Netter',
        'Trend Rider': 'Trend Rider',
        'Freedom Seeker': 'Freedom Seeker',
        'Big Dreamer': 'Big Dreamer',
        'Legacy Builder': 'Legacy Builder'
    }
    
    # Map personality
    personality_map = {
        'The Adventurer': 'Adventurer',
        'The Hedonist': 'Hedonist',
        'The Minimalist': 'Minimalist',
        'The Creator': 'Creator',
        'The Achiever': 'Achiever',
        'The Caregiver': 'Caregiver',
        'Adventurer': 'Adventurer',
        'Hedonist': 'Hedonist',
        'Minimalist': 'Minimalist',
        'Creator': 'Creator',
        'Achiever': 'Achiever',
        'Caregiver': 'Caregiver'
    }
    
    mapped_result = result.copy()
    
    # Apply mappings
    if result['archetype'] in archetype_map:
        mapped_result['archetype'] = archetype_map[result['archetype']]
    else:
        mapped_result['archetype'] = 'Safety Netter'
    
    if result['personality'] in personality_map:
        mapped_result['personality'] = personality_map[result['personality']]
    else:
        mapped_result['personality'] = 'Adventurer'
    
    return mapped_result

def store_engine1_output(user_id, result):
    """Store engine 1 results in database - UPDATED VERSION"""
    print(f"DEBUG: Attempting to store result for user {user_id}...")
    
    try:
        # Map to valid ENUM values
        mapped_result = map_to_db_enum(result)
        
        print(f"DEBUG: Original Archetype: '{result['archetype']}' -> Mapped: '{mapped_result['archetype']}'")
        print(f"DEBUG: Original Personality: '{result['personality']}' -> Mapped: '{mapped_result['personality']}'")
        
        # Direct pymysql connection (same as test_1.py)
        conn = pymysql.connect(
            host="localhost",
            user="kubyn",
            password="Venkat@3929",
            database="kubyn",
            port=3306
        )
        
        cur = conn.cursor()
        print("DEBUG: DB Connection acquired.")
        
        # UPDATED QUERY - Added run_timestamp and engine_version
        query = """
            INSERT INTO engine1_scores
            (user_id, run_timestamp, confidence_score, income_score, expense_score, 
             savings_score, archetype, personality_type, engine_version)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            run_timestamp = VALUES(run_timestamp),
            confidence_score = VALUES(confidence_score),
            income_score = VALUES(income_score),
            expense_score = VALUES(expense_score),
            savings_score = VALUES(savings_score),
            archetype = VALUES(archetype),
            personality_type = VALUES(personality_type),
            engine_version = VALUES(engine_version)
        """
        
        # Convert scores to integers for tinyint columns
        confidence_int = int(round(mapped_result["confidence_score"], 0))
        income_int = int(round(mapped_result["income_score"], 0))
        expense_int = int(round(mapped_result["expense_score"], 0))
        savings_int = int(round(mapped_result["savings_score"], 0))
        
        # Ensure within 0-100 range
        confidence_int = max(0, min(100, confidence_int))
        income_int = max(0, min(100, income_int))
        expense_int = max(0, min(100, expense_int))
        savings_int = max(0, min(100, savings_int))
        
        params = (
            user_id,
            datetime.now(),  # Current timestamp
            confidence_int,  # Converted to int
            income_int,      # Converted to int
            expense_int,     # Converted to int
            savings_int,     # Converted to int
            mapped_result["archetype"],
            mapped_result["personality"],
            1  # engine_version
        )
        
        print(f"DEBUG: Executing query with params: {params}")
        cur.execute(query, params)
        print(f"DEBUG: Query executed. Rows affected: {cur.rowcount}")
        
        conn.commit()
        print("DEBUG: Connection committed.")
        cur.close()
        conn.close()
        print("DEBUG: Connection closed. Storage successful.")
        
    except Exception as e:
        print(f"DEBUG: Error inside store_engine1_output: {e}")
        # Don't raise, just log so API doesn't crash
        print(f"⚠️  Storage failed for user {user_id}, but processing continues")

def process_multiple_users(user_dict):
    """
    user_dict = {user_id: {"user": {...}, "questions": {...}}}
    Returns results per user
    """
    results = {}
    for uid, data in user_dict.items():
        if not data["user"] or not data["questions"]:
            results[uid] = {"error": "Data not found"}
            continue
        
        result = process_engine_one(data["user"], data["questions"])
        store_engine1_output(uid, result)
        results[uid] = result
    
    return results
