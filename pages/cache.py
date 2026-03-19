import json
import os

FILE = "users.json"

def load_cache():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(FILE, "w") as f:
        json.dump(cache, f)

hashed_pw_cache = load_cache()