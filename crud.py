# crud.py
from sqlmodel import Session, select
from models.user import User
from auth import hash_password, verify_password
from typing import Optional, List
from datetime import datetime

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def create_user(session: Session, email: str, password: str, full_name: str | None = None, role = None) -> User:
    hashed = hash_password(password)
    user = User(email=email, hashed_password=hashed, full_name=full_name, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def set_password(session: Session, user: User, new_password: str):
    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user