from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas import ConversationCreate, ConversationListItem, ConversationResponse, HistoryResponse, MessageCreate, MessageResponse
from app.services.conversation_service import ConversationConflict, ConversationNotFound, ConversationService
from app.main import get_service

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate, service: ConversationService = Depends(get_service)):
    return service.create(payload.system_prompt, payload.max_turns)

@router.get("", response_model=list[ConversationListItem])
def list_conversations(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
                       service: ConversationService = Depends(get_service)):
    return service.list(limit, offset)

@router.get("/{conversation_id}", response_model=HistoryResponse)
def get_history(conversation_id: str, limit: int = Query(100, ge=1, le=500),
                offset: int = Query(0, ge=0), service: ConversationService = Depends(get_service)):
    try:
        return service.history(conversation_id, limit, offset)
    except ConversationNotFound as exc:
        raise HTTPException(404, "Conversation not found") from exc

@router.post("/{conversation_id}/messages/user", response_model=MessageResponse, status_code=201)
def add_user(conversation_id: str, payload: MessageCreate, service: ConversationService = Depends(get_service)):
    try:
        return service.append_user(conversation_id, payload.content)
    except ConversationNotFound as exc:
        raise HTTPException(404, "Conversation not found") from exc
    except ConversationConflict as exc:
        raise HTTPException(409, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.post("/{conversation_id}/messages/assistant", response_model=MessageResponse, status_code=201)
def add_assistant(conversation_id: str, payload: MessageCreate, service: ConversationService = Depends(get_service)):
    try:
        return service.append_assistant(conversation_id, payload.content)
    except ConversationNotFound as exc:
        raise HTTPException(404, "Conversation not found") from exc
    except ConversationConflict as exc:
        raise HTTPException(409, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.delete("/{conversation_id}/messages", status_code=204)
def clear_history(conversation_id: str, service: ConversationService = Depends(get_service)):
    try:
        service.clear(conversation_id)
    except ConversationNotFound as exc:
        raise HTTPException(404, "Conversation not found") from exc

@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(conversation_id: str, service: ConversationService = Depends(get_service)):
    try:
        service.delete(conversation_id)
    except ConversationNotFound as exc:
        raise HTTPException(404, "Conversation not found") from exc
