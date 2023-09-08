from database import SessionLocal
import secrets
import pyotp


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create random alphanumeric string 
def random_string(length: int = 16):        
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')          
    return ''.join(secrets.choice(letters) for i in range(length))


def generate_one_time_code(secret: str):
    totp = pyotp.TOTP(s=secret, digits=6, interval=900)
    return totp.now()


def verify_one_time_code(secret: str, one_time_code: int):
    totp = pyotp.TOTP(s=secret, digits=6, interval=900)
    return totp.verify(one_time_code)
