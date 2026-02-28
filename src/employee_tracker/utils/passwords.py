import hashlib
import os
import base64
import hmac
import binascii

def hash_password(password: str) -> str:
    # password salt created
    salt = os.urandom(16)

    # password hashed
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    )
    # resultant value needs decoding in order to be stored
    return base64.b64encode(salt + key).decode("utf-8")

# password is checked, by splitting stored hash, and using salt value to hash check value.
### AI DECLARATION - this hashing function was originally created by AI, the developer implemented once learnings had been sought on implementation of hashing and salts
def verify_password(password:str, stored_hash: str) -> bool:
    decoded = base64.b64decode(stored_hash.encode("utf-8"))
    salt = decoded[:16]
    stored_key = decoded[16:]
    new_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    )
    # stored hash and computed hash are compared and the result returned
    return hmac.compare_digest(new_key, stored_key)

# for validation, hash value is checked to validate that it follows the pattern used in above methods
def is_valid_stored_password_hash(value:str) -> bool:

    SALT_LEN = 16
    KEY_LEN = 32
    TOTAL_LEN = SALT_LEN + KEY_LEN

    if not isinstance(value,str) or not value:
        return False
    
    try:
        decoded = base64.b64decode(value, validate= True)
    except (binascii.Error, ValueError):
        return False
    
    return len(decoded) == TOTAL_LEN