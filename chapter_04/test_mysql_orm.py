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
        '''新增单条记录'''

        new_obj = News(
            title='标题',
            content='内容',
            types='百家',
        )
        self.session.add(new_obj)
        self.session.commit()

        return new_obj

    def add_more(self):
        '''新增多条记录'''

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

    def get_one(self):
        '''获取一条记录'''
        return self.session.query(News).get(122)

    def get_more(self):
        '''获取多条记录'''
        return self.session.query(News).filter_by(is_valid=1)

    def update_one(self, pk):
        '''修改一条记录'''
        if isinstance(pk, int):
            # 获取要修改的数据
            new_obj = self.session.query(News).get(pk)
        if new_obj:
            new_obj.is_valid = 0
            self.session.add(new_obj)
            self.session.commit()
            return True
        return False

    def update_more(self):
        '''修改多条记录'''
        # 获取要修改的数据
        data_list = self.session.query(News).filter_by(is_valid=1)
        if data_list:
            for item in data_list:
                item.is_valid = 0
                self.session.add(item)
            self.session.commit()
            return True
        return False

    def delete_one(self, pk):
        '''删除单条记录'''
        if isinstance(pk, int):
            # 获取要删除的数据
            new_obj = self.session.query(News).get(pk)

        if new_obj:
            self.session.delete(new_obj)
            self.session.commit()
            return True
        return False

    def delete_more(self):
        '''删除多条记录'''
        # 获取要删除的数据
        data_list = self.session.query(News).filter_by(is_valid=0)
        if data_list:
            for item in data_list:
                self.session.delete(item)
            self.session.commit()
            return True
        return False


def main():
    obj = OrmTest()
    # rest = obj.add_one()
    # print(rest[0].id)

    # rest = obj.get_one()
    # if rest:
    #     print('ID:{0} => {1}'.format(rest.id, rest.title))
    # else:
    #     print('Not exist!')

    # rest = obj.get_more()
    # print(rest.count())
    # if rest:
    #     for item in rest:
    #         print('ID:{0} => {1}'.format(item.id, item.title))
    # else:
    #     print('Not exist!')

    # print(obj.upate_data(13))

    # rest = obj.update_more()
    # print(rest)

    # rest = obj.delete_one(1)
    # print(rest)

    rest = obj.delete_more()
    print(rest)


if __name__ == '__main__':
    main()
