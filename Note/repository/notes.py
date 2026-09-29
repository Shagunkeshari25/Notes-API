from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
import json
from ..redis_client import redis_client

def clear_user_cache(user_id: int):
    keys = redis_client.keys(f"notes:user:{user_id}:*")
    if keys:
        redis_client.delete(*keys)


def get_all(db: Session, limit: int, skip: int, search: str, current_user: models.User):
    cache_key = f"notes:user:{current_user.id}:limit:{limit}:skip:{skip}:search:{search}"
    
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    query = db.query(models.Note).filter(models.Note.user_id == current_user.id)

    if search:
        query = query.filter(
            (models.Note.title.ilike(f"%{search}%")) |
            (models.Note.body.ilike(f"%{search}%"))
        )

    notes = query.limit(limit).offset(skip).all()

    notes_data = [
        {"id": n.id, "title": n.title, "body": n.body, "created_at": str(n.created_at)}
        for n in notes
    ]
    redis_client.setex(cache_key, 60, json.dumps(notes_data))

    return notes
    

# Create a new note
def create(request: schemas.NoteCreate, db: Session, current_user: models.User):  # updated
    new_note = models.Note(
        title=request.title,
        body=request.body,
        user_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    clear_user_cache(current_user.id)
    db.refresh(new_note)
    return new_note

# Delete a note by id (only if it belongs to current user)
def destroy(id: int, db: Session, current_user: models.User):  # updated
    note_query = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.user_id == current_user.id
    )
    note = note_query.first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    note_query.delete(synchronize_session=False)
    db.commit()
    clear_user_cache(current_user.id)
    return {"detail": "Note deleted"}

# Update a note by id (only if it belongs to current user)
def update(id: int, request: schemas.NoteCreate, db: Session, current_user: models.User):  # updated
    note_query = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.user_id == current_user.id
    )
    note = note_query.first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    note_query.update(request.dict())
    db.commit()
    clear_user_cache(current_user.id)
    db.refresh(note)
    return note

# Get a single note by id (only if it belongs to current user)
def show(id: int, db: Session, current_user: models.User):  # updated
    note = (
        db.query(models.Note)
        .filter(models.Note.id == id, models.Note.user_id == current_user.id)
        .first()
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note