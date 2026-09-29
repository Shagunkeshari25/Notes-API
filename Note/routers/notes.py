from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models
from ..repository import notes

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

get_db = database.get_db

# Get all notes with pagination and search
@router.get("/", response_model=List[schemas.ShowNote])
def all(
    limit: int = 10,
    skip: int = 0,
    search: str = "",            
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return notes.get_all(db, limit, skip, search, current_user)   


# Create a new note
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowNote)
def create(
    request: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  
):
    return notes.create(request, db, current_user)


# Delete a note
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  # <-- change here
):
    return notes.destroy(id, db, current_user)


# Update a note
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowNote)
def update(
    id: int,
    request: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  # <-- change here
):
    return notes.update(id, request, db, current_user)


# Get a single note
@router.get("/{id}", status_code=200, response_model=schemas.ShowNote)
def show(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  # <-- change here
):
    return notes.show(id, db, current_user)