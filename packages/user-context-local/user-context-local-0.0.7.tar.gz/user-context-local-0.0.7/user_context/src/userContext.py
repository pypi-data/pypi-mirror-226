import sys
import os
from pathlib import Path
import jwt
from dotenv import load_dotenv
script_directory = Path(__file__).resolve().parent
sys.path.append(str(script_directory))
from typing import Any
load_dotenv()

class UserContext:
    def __init__(self) -> None:
        self.user_id = None
        self.profile_id = None
        self.language = None

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def set_profile_id(self, profile_id: int) -> None:
        self.profile_id = profile_id

    def get_user_id(self) -> int:
        return self.user_id

    def get_profile_id(self) -> int:
        return self.profile_id

    def get_language(self) -> str:
        return self.language

    def set_language(self) -> None:
        return self.profile_id

    def set_jwt_token(self, jwt_token: str) -> None:
        try:
            secret_key = os.getenv("JWT_SECRET_KEY")
            decoded_payload = jwt.decode(
                jwt_token, secret_key, algorithms=['HS256'])
            # Use 'profileId' instead of 'profile_id'
            self.profile_id = int(decoded_payload.get('profileId'))
            # Use 'userId' instead of 'user_id'
            self.user_id = int(decoded_payload.get('userId'))
            self.language = decoded_payload.get('language')
        except jwt.ExpiredSignatureError:
            # Handle token expiration
            print("JWT token has expired.", sys.stderr)
            raise
        except jwt.InvalidTokenError:
            # Handle invalid token
            print("Invalid JWT token.", sys.stderr)
            raise

    @staticmethod
    def login(username: str, password: str):
        pass
