# routers/connections.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud import create_connection_request, get_pending_requests_for_user, update_connection_request_status
from models.extra import ConnectionRequest, ConnectionStatus
from deps import get_current_user
from schemas.extra import ConnectionRequestCreate

router = APIRouter()

@router.post("/request", status_code=201)
def send_connection_request(payload: ConnectionRequestCreate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Check if request already exists
    from sqlmodel import select
    existing = session.exec(
        select(ConnectionRequest).where(
            (ConnectionRequest.sender_id == current_user.id) & (ConnectionRequest.recipient_id == payload.recipient_id)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Connection request already exists")

    # Check if users are not the same
    if current_user.id == payload.recipient_id:
        raise HTTPException(status_code=400, detail="Cannot send request to yourself")

    request = create_connection_request(session, current_user.id, payload.recipient_id)
    return request

@router.get("/requests")
def get_connection_requests(current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    requests = get_pending_requests_for_user(session, current_user.id)
    return requests

@router.post("/request/{request_id}/accept", status_code=200)
def accept_connection_request(request_id: int, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    request = session.get(ConnectionRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Connection request not found")
    if request.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if request.status != ConnectionStatus.pending:
        raise HTTPException(status_code=400, detail="Request already processed")

    update_connection_request_status(session, request_id, ConnectionStatus.accepted)
    return {"message": "Connection request accepted"}

@router.post("/request/{request_id}/reject", status_code=200)
def reject_connection_request(request_id: int, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    request = session.get(ConnectionRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Connection request not found")
    if request.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if request.status != ConnectionStatus.pending:
        raise HTTPException(status_code=400, detail="Request already processed")

    update_connection_request_status(session, request_id, ConnectionStatus.rejected)
    return {"message": "Connection request rejected"}