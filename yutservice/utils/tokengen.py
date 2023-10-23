from datetime import datetime, timedelta
from yutservice.config import CONFIG
from jose import JWTError, jwt
from fastapi import HTTPException, status

ALGORITHM = "HS256"
access_token_jwt_subject = "access"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
SECRET_KEY = CONFIG['JWT_KEY']


def create_token(user_email: str) -> dict:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"email": user_email}, expires_delta=access_token_expires
        ),
        "token_type": "Bearer",
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Token creation"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")

    # if payload['exp'] <= datetime.utcnow():
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Auth token expiration")

    return payload
