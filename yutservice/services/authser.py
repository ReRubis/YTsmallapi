from google.oauth2 import id_token
from google.auth.transport import requests
from yutservice.schemas import usersschem
from yutservice.utils.repository import UserRepository
from yutservice.utils.db_session import get_db
from yutservice.models.dbmodels import User
from fastapi.exceptions import HTTPException
from fastapi import status, Header, Cookie, Depends
from yutservice.config import CONFIG
from yutservice.utils.tokengen import decode_access_token
from yutservice.schemas import reqmodel
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import requests as req
import bcrypt
import json


class CommonUserAuthenticator():
    """Object for Common Auth with password and email"""

    def __init__(self, session: Session):
        self.session = session
        self.repository = UserRepository(self.session)

    def check_password(self, request: reqmodel.RequestLogIn):
        user = self.repository.get_user(request.email)[0]
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        # Check the password
        if bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
            return True  # Correct password

        return False  # Incorrect password

    def register_new_user(self, request: reqmodel.RequestRegistration):

        if self.repository.get_user(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='User already exist')

        user = User()
        user.email = request.email
        hashed_password = bcrypt.hashpw(
            request.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')

        self.repository.save_user(user)
        return {'Message': 'Successfully registered'}

    def login_user(self, request: reqmodel.RequestLogIn):

        if self.repository.get_user(request.email):

            if not self.check_password(request):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect credentials')
            return request.email
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect credentials')

    def check_user(self, token: str) -> User:
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            decoded_jwt_token = decode_access_token(jwt_token=token)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        user = User()
        user.email = decoded_jwt_token['email']
        # user.sub = decoded_jwt_token['sub']

        user_from_db = self.repository.get_user(email=user.email)
        if user_from_db:
            return user_from_db[0]

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
