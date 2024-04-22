from typing import Annotated, Any, Dict
from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import Depends, HTTPException, Response, WebSocketException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordBearer
from datetime import datetime, timedelta, UTC
from ..schemas.auth import TokenData
from ....db.models.users import User
from ..utilities.dependency import get_db
from ..utilities.config import Settings

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes


# def create_access_token(data: dict) -> str:
def create_access_token(data: dict, res: Response) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    res.set_cookie(
        key="__Host-MyCookie1",
        # key="__Secure-MyCookie1",
        value=encoded_jwt,
        expires=expire,
        # domain="127.0.0.1",
        # path="/",
        httponly=True,
        secure=True,
        samesite="none",
        # samesite="strict",
        partitioned=True
    )
    # res.headers['Set-Cookie'] = f"{res.headers['Set-Cookie']}; Partitioned;"
    # print(res.headers.items())
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int | None = payload.get("user_id")
        # exp: float | None = payload.get("exp")
        if id is None:
            raise credentials_exception
            # raise credentials_exception["validation_error"]
        token_data = TokenData(id=id)
        # if exp is None or datetime.fromtimestamp(exp, UTC) < datetime.now(UTC):
        #     raise credentials_exception["session_closed"]
    except JWTError:
        # raise credentials_exception["validation_error"]
        raise credentials_exception
    return token_data

def verify_websocket_access(token: str, credentials_exception: WebSocketException) -> TokenData:
    try:
        if token is None:
            raise credentials_exception
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int | None = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except ExpiredSignatureError:
        raise credentials_exception
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # credentials_exception = {
    #     "validation_error": HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     ),
    #     "session_closed": HTTPException(
    #         status_code=status.HTTP_408_REQUEST_TIMEOUT,
    #         detail="Session closed, login again",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     ),
    # }
    token_asr: TokenData = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_asr.id).first()
    return user
