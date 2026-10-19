from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import database, schemas
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

# Create a new user
@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create(request, db)