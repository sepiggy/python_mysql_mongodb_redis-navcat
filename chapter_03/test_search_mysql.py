'''
查询数据
'''

import MySQLdb


class MysqlSearch():
    def __init__(self):
        self.get_conn()

    def get_conn(self):
        try:
            self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='12345', db='news', port=3306,
                                        charset='utf8')

        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def close_conn(self):
        try:
            if self.conn:
                # 关闭连接
                self.conn.close()

        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def get_one(self):
        '''
        查询一条数据
        :return:
        '''
        # 准备 SQL (防止 SQL 注入)
        sql = 'SELECT * FROM `news` WHERE `types` = %s ORDER BY `created_at` DESC;'
        # 获得 cursor
        cursor = self.conn.cursor()
        # 执行 SQL
        cursor.execute(sql, ('types1',))
        # 获取结果
        # print(dir(cursor))
        # print(cursor.description)
        rest = dict(zip([k[0] for k in cursor.description], cursor.fetchone()))
        # 获取某个字段对应的数据
        # print(type(rest))
        # print(rest)
        # print(rest['title'])

        # 关闭 cursor 和连接
        if cursor and self.conn:
            cursor.close()
            self.close_conn()

        return rest

    def get_more(self):
        '''
        查询多条数据
        :return:
        '''
        sql = 'SELECT * FROM `news` WHERE `types` = %s ORDER BY `created_at` DESC;'
        cursor = self.conn.cursor()
        cursor.execute(sql, ('types1',))
        rest = [dict(zip([k[0] for k in cursor.description], row)) for row in cursor.fetchall()]
        if cursor and self.conn:
            cursor.close()
            self.close_conn()

        return rest

    def get_more(self, page, page_size):
        '''
        分页
        :param page:
        :param page_size:
        :return:
        '''
        offset = (page - 1) * page_size
        sql = 'SELECT * FROM `news` WHERE `types` = %s ORDER BY `created_at` DESC LIMIT %s, %s;'
        cursor = self.conn.cursor()
        cursor.execute(sql, ('types1',), )
        rest = [dict(zip([k[0] for k in cursor.description], row)) for row in cursor.fetchall()]
        if cursor and self.conn:
            cursor.close()
            self.close_conn()

        return rest


def main():
    obj = MysqlSearch()
    # rest = obj.get_one()
    # print(rest['title'])
    rest = obj.get_more()
    for item in rest:
        print(item)
        print('-------')


if __name__ == '__main__':
    main()
