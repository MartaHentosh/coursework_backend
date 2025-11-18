from fastapi import APIRouter, Depends, HTTPException, Query, Path
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
from pydantic import BaseModel

from database import SessionLocal
import models

from uuid import UUID
import json
from datetime import datetime


router = APIRouter(
    prefix='/home',
    tags=['home']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CategoryResponse(BaseModel):
    id: int
    name: str
    image_url: str

    class Config:
        from_attributes = True


class TextFilterResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    rating: float
    delivery_time: Optional[int]
    delivery_fee: float
    min_order: float
    distance: float

    class Config:
        from_attributes = True


class SortOptionResponse(BaseModel):
    id: str
    name: str
    field: str
    order: str

    class Config:
        from_attributes = True


class SaveFilterRequest(BaseModel):
    category_ids: Optional[List[int]] = None
    text_filter_ids: Optional[List[int]] = None

class SaveFilterResponse(BaseModel):
    search_id: str


class DishResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    weight: Optional[float]
    image_url: Optional[str]

    class Config:
        from_attributes = True


class RestaurantDetailsResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    rating: float
    delivery_time: Optional[int]
    dishes: List[DishResponse]

    class Config:
        from_attributes = True


@router.get("/restaurants", response_model=List[RestaurantResponse], status_code=status.HTTP_200_OK)
async def get_all_restaurants(db: db_dependency):

    restaurants = db.query(models.Restaurant).filter(models.Restaurant.is_active == 1).all()
    return restaurants



@router.get("/restaurants/sort-by", response_model=List[RestaurantResponse], status_code=status.HTTP_200_OK)
async def get_restaurants_sorted(
    db: db_dependency,
    sort_by: str = Query(..., description="Сортування командами: distance_asc/desc, rating_asc/desc, delivery_fee_asc/desc")
):

    query = db.query(models.Restaurant).filter(models.Restaurant.is_active == 1)

    query = apply_sorting(query, sort_by)
    
    restaurants = query.all()
    return restaurants


@router.post("/restaurants/save-filtered", response_model=SaveFilterResponse, status_code=status.HTTP_201_CREATED)
async def save_filtered_restaurants(
    request: SaveFilterRequest,
    db: db_dependency
):
    if not request.category_ids and not request.text_filter_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Потрібно передати номер id category та/або text_filter")

    if request.category_ids:
        validate_categories(db, request.category_ids)
    if request.text_filter_ids:
        validate_text_filters(db, request.text_filter_ids)

    query = db.query(models.Restaurant).filter(models.Restaurant.is_active == 1)

    if request.category_ids:
        query = query.join(models.Restaurant.categories).filter(models.Category.id.in_(request.category_ids))

    if request.text_filter_ids:
        query = query.join(models.Restaurant.text_filters).filter(models.TextFilter.id.in_(request.text_filter_ids))

    query = query.distinct()
    restaurants = query.all()
    restaurant_ids = [r.id for r in restaurants]

    saved = models.SavedSearch(
        category_ids=request.category_ids,
        text_filter_ids=request.text_filter_ids,
        restaurant_ids=restaurant_ids
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)

    return SaveFilterResponse(search_id=saved.id)


@router.get("/restaurants/sort-filtered", response_model=List[RestaurantResponse], status_code=status.HTTP_200_OK)
async def get_saved_restaurants(
    search_id: str,
    db: db_dependency,
    sort_by: Optional[str] = Query(None, description="Сортування командами: distance_asc/desc, rating_asc/desc, delivery_fee_asc/desc")
):
    saved = db.query(models.SavedSearch).filter(models.SavedSearch.id == search_id).first()
    if not saved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved search не знайдено")

    if not saved.restaurant_ids:
        return []

    query = db.query(models.Restaurant).filter(models.Restaurant.id.in_(saved.restaurant_ids))

    query = apply_sorting(query, sort_by)

    restaurants = query.all()

    if not sort_by:
        id_to_rest = {r.id: r for r in restaurants}
        ordered = [id_to_rest[rid] for rid in saved.restaurant_ids if rid in id_to_rest]
        return ordered

    return restaurants


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantDetailsResponse)
async def get_restaurant_details(
        restaurant_id: int = Path(..., description="ID ресторану"),
        db: db_dependency = None
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Ресторан не знайдено")

    # Обираємо 6 випадкових страв цього ресторану
    dishes_qs = db.query(models.Dish).filter(models.Dish.restaurant_id == restaurant_id).limit(6).all()
    dishes = [DishResponse.from_orm(d) for d in dishes_qs]

    response = RestaurantDetailsResponse(
        id=restaurant.id,
        name=restaurant.name,
        description=restaurant.description,
        image_url=restaurant.image_url,
        rating=restaurant.rating,
        delivery_time=restaurant.delivery_time,
        dishes=dishes
    )
    return response


def apply_sorting(query, sort_by: Optional[str] = None):

    if not sort_by:
        return query

    sort_mapping = {
        "distance_asc": models.Restaurant.distance.asc(),
        "distance_desc": models.Restaurant.distance.desc(),
        "rating_asc": models.Restaurant.rating.asc(),
        "rating_desc": models.Restaurant.rating.desc(),
        "delivery_fee_asc": models.Restaurant.delivery_fee.asc(),
        "delivery_fee_desc": models.Restaurant.delivery_fee.desc(),
    }

    if sort_by in sort_mapping:
        return query.order_by(sort_mapping[sort_by])

    return query


def validate_categories(db: Session, category_ids: List[int]):
    categories = db.query(models.Category).filter(models.Category.id.in_(category_ids)).all()
    if len(categories) != len(category_ids):
        found_ids = [cat.id for cat in categories]
        missing_ids = [cid for cid in category_ids if cid not in found_ids]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Не існує категорій з ID {missing_ids}"
        )
    return categories


def validate_text_filters(db: Session, text_filter_ids: List[int]):
    text_filters = db.query(models.TextFilter).filter(models.TextFilter.id.in_(text_filter_ids)).all()
    if len(text_filters) != len(text_filter_ids):
        found_ids = [tf.id for tf in text_filters]
        missing_ids = [tfid for tfid in text_filter_ids if tfid not in found_ids]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Нема текст. фільтрів з ID {missing_ids}"
        )
    return text_filters


