import bcrypt, hashlib

# --- HASHING HELPERS (FIXED & MODERN) ---
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hash. 
    1. Pre-hashes plain_password to SHA-256 (handles 72-byte limit).
    2. Checks against the bcrypt hash.
    """
    # 1. SHA-256 Pre-hashing
    password_digest = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    
    # 2. Bcrypt Check
    # bcrypt.checkpw requires BYTES for both arguments.
    # We assume hashed_password is stored as a string in DB, so we encode it.
    return bcrypt.checkpw(
        password_digest.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

async def get_password_hash(password: str) -> str:
    """
    Generates a secure password hash.
    1. Pre-hashes to SHA-256.
    2. Hashes with Bcrypt + Salt.
    """
    # 1. SHA-256 Pre-hashing
    password_digest = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # 2. Bcrypt Hash
    # bcrypt.hashpw returns bytes. We .decode('utf-8') to store it as a string in MongoDB.
    hashed_bytes = bcrypt.hashpw(password_digest.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')