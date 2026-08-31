from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config.config_loader import Config
import jwt

SECRET_KEY = Config.get("SECRET_KEY")
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return {"username": payload["sub"], "role": payload.get("role", "standard")}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

def generate_token(username, role="standard"):
    payload = {
        'exp': jwt.datetime.datetime.utcnow() + jwt.datetime.timedelta(days=1),
        'sub': username,
        'role': role
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
