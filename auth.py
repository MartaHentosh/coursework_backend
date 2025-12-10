from datetime import timedelta, datetime
from typing import Annotated
from starlette import status
from database import SessionLocal
from models import Users
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import re


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'fhi3uo2hr2h3iu5rhiu32ph52hrhf'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(db: db_dependency,
                      register_request: RegisterRequest):
    username = register_request.username
    password = register_request.password

    if len(username) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 4 characters long"
        )

    if len(password) < 4 or not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your password must be 4+ characters long and have at least one digit"
        )

    register_model = Users(
        username=register_request.username,
        email=register_request.email,
        hashed_password=bcrypt_context.hash(register_request.password),
    )

    db.add(register_model)
    db.commit()
    db.refresh(register_model)

@router.post("/login", response_model=Token)
async def login_with_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, timedelta(minutes=45))

    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username:str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id':user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
