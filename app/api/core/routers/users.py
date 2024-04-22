from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas.users import UserOut, UserCreate
from ..utilities.dependency import get_db
from ..utilities.tools import hash
from ....db.models.users import User
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
async def get_users(
    db: Annotated[Session, Depends(get_db)],
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
) -> List[User]:
    users = (
        db.query(User)
        .filter(User.email.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: int, db: Annotated[Session, Depends(get_db)]) -> User:
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} is not found",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]) -> User:
    # print(user)
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
