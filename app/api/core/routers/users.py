from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas.users import UserOut, UserCreate
from ..utilities.dependency import get_db
from ..utilities.tools import hash
from ....db.models.users import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
# async def get_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} is not found",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
