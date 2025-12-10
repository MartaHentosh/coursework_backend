from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Users
from auth import get_current_user
from database import SessionLocal


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_admin_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user['id']).first()
    if not db_user or not getattr(db_user, 'is_admin', 0):
        raise HTTPException(status_code=403, detail="Admin only")
    return db_user


@router.get('/users', response_model=List[dict])
def get_users(admin: Users = Depends(get_admin_user), db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return [
        {"id": userino.id, "username": userino.username, "email": userino.email, "is_admin": userino.is_admin}
        for userino in users
    ]


@router.put('/users/{user_id}')
def edit_user(user_id: int, username: Optional[str] = None, email: Optional[str] = None, is_admin: Optional[int] = None, admin: Users = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    if username:
        user.username = username
    if email:
        user.email = email
    if is_admin is not None:
        user.is_admin = is_admin
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin}


@router.delete('/users/{user_id}')
def delete_user(user_id: int, admin: Users = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}
