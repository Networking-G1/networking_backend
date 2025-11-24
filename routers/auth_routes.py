# routers/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud import authenticate_user
from auth import create_access_token
from schemas.schemas import Token
from typing import Dict

router = APIRouter()

@router.post("/token", response_model=Token)
def login(form_data: Dict[str, str], session: Session = Depends(get_session)):
    username = form_data.get("username") or form_data.get("email")
    password = form_data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Credenciales incompletas")

    user = authenticate_user(session, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token, expires_in = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer", "expires_in": expires_in}
