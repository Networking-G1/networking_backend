# routers/messages.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, or_, and_
from typing import List
from models.message import Message
from models.user import User
from schemas.message import MessageCreate, MessageResponse, ConversationResponse, UserBasic
from deps import get_current_user, get_db_session
from datetime import datetime

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session)
):
    """
    Obtener lista de conversaciones del usuario autenticado.
    Devuelve el otro usuario y el último mensaje de cada conversación.
    """
    # Obtener todos los usuarios con los que el usuario actual ha tenido conversaciones
    # Buscar mensajes donde el usuario es emisor o receptor
    statement = select(Message).where(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).order_by(Message.created_at.desc())
    
    messages = session.exec(statement).all()
    
    # Agrupar por conversación (por el otro usuario)
    conversations_dict = {}
    
    for message in messages:
        # Determinar quién es el otro usuario
        other_user_id = message.receiver_id if message.sender_id == current_user.id else message.sender_id
        
        # Si no hemos visto esta conversación, agregarla
        if other_user_id not in conversations_dict:
            # Obtener información del otro usuario
            other_user = session.get(User, other_user_id)
            if other_user:
                conversations_dict[other_user_id] = {
                    "other_user": other_user,
                    "last_message": message
                }
    
    # Convertir a lista de ConversationResponse
    conversations = []
    for conv_data in conversations_dict.values():
        conversations.append(ConversationResponse(
            other_user=UserBasic(
                id=conv_data["other_user"].id,
                full_name=conv_data["other_user"].full_name,
                email=conv_data["other_user"].email
            ),
            last_message=MessageResponse.model_validate(conv_data["last_message"])
        ))
    
    return conversations


@router.get("/{user_id}", response_model=List[MessageResponse])
async def get_messages(
    user_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session)
):
    """
    Obtener mensajes de una conversación específica con otro usuario.
    Devuelve los mensajes ordenados por fecha (más antiguos primero).
    """
    # Verificar que el otro usuario existe
    other_user = session.get(User, user_id)
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Obtener mensajes entre los dos usuarios
    statement = select(Message).where(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).limit(limit)
    
    messages = session.exec(statement).all()
    
    return [MessageResponse.model_validate(msg) for msg in messages]


@router.post("/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session)
):
    """
    Enviar un nuevo mensaje a otro usuario.
    """
    # Validar que el receptor existe
    receiver = session.get(User, message_data.receiver_id)
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario receptor no encontrado"
        )
    
    # Validar que no se envíe mensaje a sí mismo
    if message_data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes enviarte mensajes a ti mismo"
        )
    
    # Validar que el contenido no esté vacío
    if not message_data.content or not message_data.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El contenido del mensaje no puede estar vacío"
        )
    
    # Crear el mensaje
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=message_data.receiver_id,
        content=message_data.content.strip(),
        file_url=message_data.file_url,
        created_at=datetime.utcnow(),
        read=False
    )
    
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    
    return MessageResponse.model_validate(new_message)


@router.put("/{sender_id}/read", status_code=status.HTTP_200_OK)
async def mark_messages_as_read(
    sender_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session)
):
    """
    Marcar todos los mensajes de un usuario específico como leídos.
    """
    # Verificar que el emisor existe
    sender = session.get(User, sender_id)
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Buscar todos los mensajes no leídos del sender al current_user
    statement = select(Message).where(
        and_(
            Message.sender_id == sender_id,
            Message.receiver_id == current_user.id,
            Message.read == False
        )
    )
    
    messages = session.exec(statement).all()
    
    # Marcar todos como leídos
    updated_count = 0
    for message in messages:
        message.read = True
        session.add(message)
        updated_count += 1
    
    session.commit()
    
    return {
        "message": "Mensajes marcados como leídos",
        "updated_count": updated_count
    }
