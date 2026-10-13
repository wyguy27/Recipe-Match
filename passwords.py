import bcrypt

def hash_password(pw_text):
    #convert to Bytes
    pw_bytes = pw_text.encode('utf-8')
    salt = bcrypt.gensalt(rounds = 12)
    pw_hashed = bcrypt.hashpw(pw_bytes, salt)
    return pw_hashed