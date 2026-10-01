from sqlalchemy.orm import Session
from .. import models, schemas
from ..hashing import Hash


def create(request: schemas.UserCreate, db: Session):
    # Hash the password before storing
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

