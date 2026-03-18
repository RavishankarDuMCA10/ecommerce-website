from fastapi import HTTPException, Request
import jwt
from config.Env import ENVConfig


def verifyToken(req: Request):
    authorization = req.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please Login First")

    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Please provide valid token")
    try:
        payload = jwt.decode(
            token, ENVConfig.JWT_AUTH_SECRET_KEY, algorithms=[ENVConfig.ALGORITHMS]
        )
        return payload["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"{e}")
