# coding: utf-8
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

# 数据库实体模型
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    mid = Column(VARCHAR(255), nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    genres = Column(VARCHAR(255), nullable=False)


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    uid = Column(VARCHAR(255), nullable=False)
    mid = Column(VARCHAR(255), nullable=False)
    rates = Column(VARCHAR(255), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uid = Column(VARCHAR(255), nullable=False)
    gender = Column(VARCHAR(255), nullable=False)
    age = Column(VARCHAR(255), nullable=False)
    occupation = Column(VARCHAR(255), nullable=False)
