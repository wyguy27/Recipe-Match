import bcrypt

def hash_password(pw_text):
    #convert to Bytes
    pw_bytes = pw_text.encode('utf-8')
    salt = bcrypt.gensalt(rounds = 12)
    pw_hashed = bcrypt.hashpw(pw_bytes, salt)
    return pw_hashed

def verify_password(pw_text, pw_hashed):
    return bcrypt.checkpw(pw_text.encode('utf-8'), pw_hashed)