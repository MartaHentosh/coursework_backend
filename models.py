from database import Base
from sqlalchemy import String, Integer, Column, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from sqlalchemy import JSON, DateTime

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Integer, default=0)


restaurant_category_table = Table(
    'restaurant_category',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

restaurant_text_filter_table = Table(
    'restaurant_text_filter',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'), primary_key=True),
    Column('text_filter_id', Integer, ForeignKey('text_filters.id'), primary_key=True)
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    image_url = Column(String, nullable=False)
    restaurants = relationship('Restaurant', secondary=restaurant_category_table, back_populates='categories')


class TextFilter(Base):
    __tablename__ = 'text_filters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    restaurants = relationship('Restaurant', secondary=restaurant_text_filter_table, back_populates='text_filters')


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    image_url = Column(String)
    rating = Column(Float, default=0.0)
    delivery_time = Column(Integer)
    delivery_fee = Column(Float, default=0.0)
    min_order = Column(Float, default=0.0)
    distance = Column(Float, default=0.0)
    is_active = Column(Integer, default=1)
    
    categories = relationship('Category', secondary=restaurant_category_table, back_populates='restaurants')
    text_filters = relationship('TextFilter', secondary=restaurant_text_filter_table, back_populates='restaurants')
    dishes = relationship('Dish', back_populates='restaurant')


class SavedSearch(Base):
    __tablename__ = 'saved_searches'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category_ids = Column(JSON, nullable=True)
    text_filter_ids = Column(JSON, nullable=True)
    restaurant_ids = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)

    restaurant = relationship('Restaurant', back_populates='dishes')


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    user = relationship('Users')
    dish = relationship('Dish')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order = relationship('Order', back_populates='items')
    dish = relationship('Dish')