from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

# 获取连接
engine = create_engine('mysql://root:12345@localhost:3306/news_test')

# 声明 Mapping
Base = declarative_base()


class News(Base):
    __tablename__ = 'news'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(200), nullable=False)
    content = Column('content', String(2000), nullable=False)
    types = Column('types', String(10), nullable=False)
    image = Column('image', String(300), nullable=True)
    author = Column('author', String(20), nullable=True)
    view_count = Column('count', Integer, default=0)
    created_at = Column('created_at', DateTime, nullable=True)
    is_valid = Column('is_valid', Boolean)
