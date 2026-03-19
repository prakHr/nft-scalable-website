import json
import os
import hashlib
from cryptography.fernet import Fernet
import base64
# --- Secret ---
SECRET = os.environ.get("CACHE_SECRET", "mysecretkey")

# --- Generate filename ---
def get_filename():
    name = hashlib.sha256(SECRET.encode()).hexdigest()
    return f".{name}.dat"

FILE = get_filename()

# --- Generate encryption key ---
def get_key():
    return hashlib.sha256(SECRET.encode()).digest()

fernet = Fernet(base64.urlsafe_b64encode(get_key()))

def load_cache():
    if os.path.exists(FILE):
        with open(FILE, "rb") as f:
            encrypted = f.read()
            decrypted = fernet.decrypt(encrypted)
            return json.loads(decrypted.decode())
    return {}

def save_cache(cache):
    data = json.dumps(cache).encode()
    encrypted = fernet.encrypt(data)
    with open(FILE, "wb") as f:
        f.write(encrypted)

hashed_pw_cache = load_cache()