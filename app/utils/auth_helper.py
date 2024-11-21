from flask_jwt_extended import create_access_token, create_refresh_token

def generate_tokens(user_id):
    access_token = create_access_token(identity=user_id, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(identity=user_id)
    return access_token, refresh_token
