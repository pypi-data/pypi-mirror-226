import jwt
import os
import sys
from dotenv import load_dotenv
load_dotenv()

def get_profile_and_user_id_from_jwt_Token(jwt_token)->(int,int,str):
    try:
        secret_key = os.getenv("JWT_SECRET_KEY")
        decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        profile_id = decoded_payload.get('profileId')  # Use 'profileId' instead of 'profile_id'
        user_id = decoded_payload.get('userId')  # Use 'userId' instead of 'user_id'
        language=decoded_payload.get('language')
        return user_id,profile_id,language
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        print("JWT token has expired.",sys.stderr)
        return None, None,None
    except jwt.InvalidTokenError:
        # Handle invalid token
        print("Invalid JWT token.",sys.stderr)
        return None, None, None





