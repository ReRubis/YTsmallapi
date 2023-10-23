from fastapi import APIRouter, HTTPException, Request,\
    Depends, Header, Response, status


from google.oauth2 import id_token
from google.auth.transport import requests

from googleapiclient.discovery import build
from yutservice.services.authser import CommonUserAuthenticator
from yutservice.schemas import respmodel, usersschem, reqmodel
from yutservice.models.dbmodels import User
from yutservice.utils.tokengen import create_token
from yutservice.routes.injectors import get_auth_user, get_common_auth_service
router = APIRouter(
    prefix='/auth',
    tags=["auth"],
)


@router.get('/logout')
async def logout(
    response: Response,
):
    """Sets auth cookie to None"""
    response.set_cookie(key="auth", value=None,
                        samesite='none', secure=True, httponly=True)
    return {'Message': 'Done'}


@router.get('/login_check',
            response_model=usersschem.UserOut)
async def check_login(
    user: User = Depends(get_auth_user),
):
    """
    This endpoint gets called when the website loads
    to check if the user is logged in, if the cookie is valid

    If no, endpoint returns a 400 and the user is asked to log in or register on the frontend. 
    If yes, it returns a user data needed for profile load
    """
    return user


@router.post('/sign_up')
async def register_new_user(
    request: reqmodel.RequestRegistration,
    service: CommonUserAuthenticator = Depends(get_common_auth_service),
):
    """Registers a user by provided password, email, company, phone, code"""

    return service.register_new_user(request)


@router.post('/sign_in')
async def sign_in(
    response: Response,
    request: reqmodel.RequestLogIn,
    service: CommonUserAuthenticator = Depends(get_common_auth_service),
):
    """Login by email and password"""
    email = service.login_user(request)

    jwt_token = create_token(email)
    response.set_cookie(key="auth", value=jwt_token['access_token'],
                        samesite='none', secure=True, httponly=True)
    return {'message': 'Successfully loggedin'}
