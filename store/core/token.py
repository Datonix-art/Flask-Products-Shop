from flask import current_app
from itsdangerous import URLSafeTimedSerializer

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(email, salt=current_app.config.get('SECURITY_PASSWORD_SALT'))

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    try:
        email = serializer.loads(
            token, salt=current_app.config.get('SECURITY_PASSWORD_SALT'), max_age=expiration
        )
        return email
    except Exception:
        return False
    
