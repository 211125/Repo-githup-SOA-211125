import secrets

def generate_secret_key():
    return secrets.token_hex(32)

SECRET_KEY = generate_secret_key()

print(generate_secret_key())
