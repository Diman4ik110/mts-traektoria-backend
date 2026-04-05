import jwt
from jwt.exceptions import PyJWTError, InvalidTokenError, ExpiredSignatureError
import time
from typing import Dict, Any, List, Optional
from app.core.config import Config

config = Config()
# Генерация токена argon2
def generateJWTToken(
    payload: Dict[str, Any]
) -> str:
    # Добавляем время истечения
    payload['exp'] = int(time.time()) + config.JWT_EXPIRATION_TIME * 3600
    
    # Добавляем время создания (опционально)
    payload['iat'] = int(time.time())
    # Генерируем токен
    token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
    return token

def decodeJWTToken(token: str) -> Dict[str, Any]:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=config.SECRET_KEY,
            algorithms=["HS256"]
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise PyJWTError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise PyJWTError(f"Invalid token: {str(e)}")

# Проверка, что токен действителен
def isJWTTokenValid(token: str) -> bool:
    try:
        decodeJWTToken(token)
        return True
    except PyJWTError:
        return False
    except InvalidTokenError:
        return False
    except ExpiredSignatureError:
        return False