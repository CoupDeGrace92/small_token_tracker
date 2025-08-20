import json
import os
from datetime import datetime, timedelta

TOKEN_LOG_FILE = 'token_log.json'
DAILY_RESET = '2025-08-21T01:00:00'  # PUT YOUR DEFAULT ai_reset time HERE OR DIRECTLY IN THE JSON FILE - make sure this is the NEXT reset

def get_current_token_totals():
    if os.path.exists(TOKEN_LOG_FILE):
        with open(TOKEN_LOG_FILE, 'r') as f:
            data = json.load(f)
            if "ai_reset_time" in data and data["ai_reset_time"]:
                data["ai_reset_time"] = datetime.fromisoformat(data["ai_reset_time"])
            else:
                data["ai_reset_time"] = DAILY_RESET 
            if "last_reset" in data and data["last_reset"]:
                data["last_reset"] = datetime.fromisoformat(data["last_reset"])
            else:
                data["last_reset"] = None
            return data
    return {"total_prompt_tokens": 0, "total_candidates_tokens": 0, "total_RPD": 0, "daily_prompt_tokens": 0, "daily_candidates_tokens": 0, "daily_RPD": 0, "last_reset": None, "ai_reset_time": DAILY_RESET}

def save_new_token_totals(totals):
    data_to_save = totals.copy()
    if "ai_reset_time" in data_to_save and isinstance(data_to_save["ai_reset_time"], datetime):
        data_to_save["ai_reset_time"] = data_to_save["ai_reset_time"].isoformat()
    if "last_reset" in data_to_save and isinstance(data_to_save["last_reset"], datetime):
        data_to_save["last_reset"] = data_to_save["last_reset"].isoformat()
    with open(TOKEN_LOG_FILE, 'w') as f:
        json.dump(data_to_save, f, indent = 2)

def update_token_totals(prompt_tokens, candidate_tokens):
    resetter()
    current_totals = get_current_token_totals()
    current_totals["total_prompt_tokens"] += prompt_tokens
    current_totals["total_candidates_tokens"] += candidate_tokens
    current_totals["total_RPD"] += 1
    current_totals["daily_prompt_tokens"] += prompt_tokens
    current_totals["daily_candidates_tokens"] += candidate_tokens
    current_totals["daily_RPD"] += 1
    save_new_token_totals(current_totals)

def resetter():
    try:
        current_totals = get_current_token_totals()
        reset_time = current_totals.get("ai_reset_time")
        if reset_time is None:
            raise Exception("Remember to set the time the used AI resets its RPD count and token use count")
        right_now = datetime.now()    
        if reset_time < right_now:
            current_totals["daily_prompt_tokens"] = 0
            current_totals["daily_candidates_tokens"] = 0
            current_totals["daily_RPD"] = 0
            while reset_time < right_now:
                reset_time += timedelta(days=1)
            current_totals["ai_reset_time"] = reset_time.isoformat()
            current_totals["last_reset"] = right_now.isoformat()
            save_new_token_totals(current_totals)
            print("Daily tokens reset")
        else:
            print("Not time to reset")
    except Exception as e:
        print(f"{e} - resetter will not operate" )


