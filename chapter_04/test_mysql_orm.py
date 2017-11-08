from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 获取连接
engine = create_engine('mysql://root:12345@localhost:3306/news_test?charset=utf8')

# 声明 Mapping
Base = declarative_base()

Session = sessionmaker(bind=engine)


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


class OrmTest(object):
    def __init__(self):
        self.session = Session()

    def add_one(self):
        '''
        新增记录
        :return:
        '''
        new_obj = News(
            title='标题',
            content='内容',
            types='百家',
        )
        new_obj2 = News(
            title='标题',
            content='内容',
            types='百家',
        )
        self.session.add(new_obj)
        self.session.add(new_obj2)
        self.session.commit()

        return new_obj, new_obj2


def main():
    obj = OrmTest()
    rest = obj.add_one()
    print(rest[0].id)


if __name__ == '__main__':
    main()
