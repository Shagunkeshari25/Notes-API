from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, schemas
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

# Create a new user
@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create(request, db)

