# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Any
from database import get_session
from schemas import UserCreate, UserRead
from crud import create_user, get_user_by_email, set_password
from deps import get_current_user
from auth import create_access_token, decode_token
from datetime import timedelta
from models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    existing = get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = create_user(
        session,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        role=user_in.role,
    )
    return user

@router.post("/recover")
def recover_account(payload: dict, session: Session = Depends(get_session)):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email requerido")
    user = get_user_by_email(session, email)
    if not user:
        return {"ok": True}  # No revelar si el email existe
    token, expires_in = create_access_token(subject=user.id, expires_delta=timedelta(minutes=15))
    # Aquí puedes enviar el token por correo
    return {"reset_token": token, "expires_in": expires_in}

@router.post("/reset-password")
def reset_password(payload: dict, session: Session = Depends(get_session)):
    token = payload.get("token")
    new_password = payload.get("new_password")
    if not token or not new_password:
        raise HTTPException(status_code=400, detail="token y new_password requeridos")
    payload_decoded = decode_token(token)
    if not payload_decoded:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    sub = payload_decoded.get("sub")
    if not sub:
        raise HTTPException(status_code=400, detail="Token inválido")
    user = session.get(User, int(sub))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    set_password(session, user, new_password)
    return {"ok": True}

@router.get("/me", response_model=UserRead)
def read_me(current_user = Depends(get_current_user)):
    return current_user
