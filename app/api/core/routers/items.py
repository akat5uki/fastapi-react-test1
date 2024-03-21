from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..schemas.items import ItemOut, Item_s, ItemCreate
from ....db.models.users import User
from ....db.models.items import Item
from ..utilities.dependency import get_db
from ..utilities.oauth2 import get_current_user


router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ItemOut])
async def get_items(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    items = (
        db.query(Item, func.count().label("zcount"))
        .filter(Item.owner_id == current_user.id, Item.title.contains(search))
        .group_by(Item.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    items = list(map(lambda x: x._mapping, items))
    return items


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Item_s)
async def create_items(
    item: ItemCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    new_item = Item(owner_id=current_user.id, **item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ItemOut)
async def get_item(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    item = (
        db.query(Item, func.count().label("zcount"))
        .filter(Item.owner_id == current_user.id, Item.id == id)
        .group_by(Item.id)
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {id} is not found",
        )
    item = item._mapping
    return item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    item_query = db.query(Item).filter(Item.id == id)
    item: Item = item_query.first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {id} does not exists",
        )
    item_auth: Item = item_query.filter(Item.owner_id == current_user.id).first()
    if item_auth is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    item_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Item_s)
async def update_item(
    id: int,
    item: ItemCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    item_query = db.query(Item).filter(Item.id == id)
    item_set: Item = item_query.first()
    if item_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {id} does not exists",
        )
    item_auth: Item = item_query.filter(Item.owner_id == current_user.id).first()
    if item_auth is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    vals: Dict[Any, Any] = item.model_dump()
    item_query.update(
        values=vals, synchronize_session=False
    )
    db.commit()
    item_set = item_query.first()
    return item_set
