'''
连接数据库
'''

import MySQLdb

try:
    # 获取连接
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='12345', db='news', port=3306, charset='utf8')

    # 获取数据
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `news` ORDER BY `created_at` DESC;')
    rest = cursor.fetchone()
    print(rest)

    # 关闭连接
    conn.close()
except MySQLdb.Error as e:
    print('Error: %s' % e)
