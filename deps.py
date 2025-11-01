# deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token
from database import get_session
from sqlmodel import Session
from crud import get_user
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db_session():
    yield from get_session()

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db_session)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = get_user(session, int(sub))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
    return user
