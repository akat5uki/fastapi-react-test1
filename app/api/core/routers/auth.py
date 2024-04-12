from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ..schemas.auth import Token
from ..utilities.dependency import get_db
from ..utilities.tools import verify
from ..utilities.oauth2 import create_access_token
from ....db.models.users import User

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=Token)
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    response: Response,
):
    """`Login Endpoint` - _This endpoint is used to generate JWT token which can later be used for authentication._

    Args:

        user_credentials (Annotated[OAuth2PasswordRequestForm, Depends): OAuth2 dependency
        db (Annotated[Session, Depends): Database session dependency
        response (Response): Response header

    Raises:

        HTTPException: Invalid Credentials (Status code: 403)
        HTTPException: Invalid Credentials (Status code: 403)

    Returns:

        dict(str, str): Respond body
    """
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    access_token = create_access_token(data={"user_id": user.id}, res=response)
    # access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
