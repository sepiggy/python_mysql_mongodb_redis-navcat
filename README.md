## 一 Python 操作 MySQL
### (一) SQL 语法基础
1. DDL (数据定义语句)
    - CREATE TABLE/DATABASE
        - 创建数据表时最好显示指定字符编码
            ```sql
            DEFAULT CHARSET 'UTF8'
            ```
            
        - SQL 语句的变量名尽量使用 `` 包裹起来, 避免与 SQL 的关键字重复
            
    - ALTER TABLE/DATABASE
    
    - DROP TABLE/DATABASE
    
2. DML (数据管理语句)
    - INSERT 新增
        - 关键字 `INSERT INTO`, `VALUE(S)` (有序)
        - INSERT INTO 语句最好指定插入的字段
        
    - DELETE 删除 (物理删除)
        - 关键字 `DELETE FROM`, `WHERE` (有序)
        - DELETE FROM 语句一定要写 WHERE 条件
        - 实际开发中多通过添加一个 `is_valid` 字段来实现 `逻辑删除`
        
    - UPDATE 修改
        - 关键字 `UPDATE`, `SET`, `WHERE` (有序)
        - UPDATE 语句一定要写 WHERE 条件
        
    - SELECT 查询
        - 关键字 `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT` (有序)
        - SELECT 语句尽量指定列名查询, 而不用 `SELECT *`
        
### (二) mysql-client API
1. 环境配置以及依赖安装
    - python 3
    - mysql
    - pip
    - virtualenv
    - pip install mysql-client
    
2. 获取数据库连接
    - 利用 `mysql-client` 连接 MySQL, 需要提供必要的连接参数, 如下所示
    ```python
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='12345', db='news', port=3306, charset='utf8')
    ```

3. 查询操作
    - 在获取完数据库的连接的基础上, 可以进行查询操作
    
    - 查询操作的大致步骤如下:
        - 准备 SQL
        - 获取 cursor
        - 执行 SQL
        - 获取执行结果
        - 处理结果
        - 关闭 cursor 和连接
        ```python
        # 准备 SQL (防止 SQL 注入)
        sql = 'SELECT * FROM `news` WHERE `types` = %s ORDER BY `created_at` DESC;'
        # 获得 cursor
        cursor = self.conn.cursor()
        # 执行 SQL
        cursor.execute(sql, ('types1',))
        # 获取和处理结果
        rest = dict(zip([k[0] for k in cursor.description], cursor.fetchone()))
        # 关闭 cursor 和连接
        if cursor and self.conn:
            cursor.close()
            self.close_conn() 
        ```
    - `mysql-client` 提供的查询函数
        - Cursor.fetchone(): 获取一条查询记录
        - Cursor.fetchall(): 获取多条查询记录
        - Cursor.description: 获取查询字段
        
4. 增删改操作
    - 增删改操作, 会对数据库进行修改, 涉及到事务操作
        - Cursor.commit(): 提交事务
        - Cursor.rollback(): 回滚事务
    
    - 最佳实践 
        - 事务提交操作放在 `try` 语句块中
        - 事务回滚操作放在 `except` 语句块中
        - 关闭 Cursor 和数据库连接操作放到 `finally` 语句块中
        - 一个例子
            ```python
            def add_one(self):
                # 准备 SQL
                try:
                    sql = (
                        "INSERT INTO `news`(`title`, `image`, `content`, `types`, `is_valid`) "
                        "VALUE(%s, %s, %s, %s, %s);"
                    )

                    # 获取连接和 cursor
                    conn = self.conn
                    cursor = conn.cursor()

                    # 执行 SQL
                    # 提交数据到数据库
                    cursor.execute(sql, ('标题11', '/static/img/news/01.png', '新闻内容5', '推荐', 1))
                    # 1 / 0
                    cursor.execute(sql, ('标题12', '/static/img/news/01.png', '新闻内容6', '推荐', 1, 'hello'))

                    # 提交事务, 不加下面这行数据不会真正写到数据库里, 会发生事务回滚
                    self.conn.commit()

                except:
                    print('error')
                    # 部分提交
                    # self.conn.commit()

                    # 回滚事务
                    self.conn.rollback()
                finally:
                    # 关闭 cursor 和 连接
                    cursor.close()
                    self.close_conn()
            ```
            
### (三) ORM
1. ORM 介绍
    - Python 中 ORM 的主要实现
        - SqlObject
        - peewee
        - Django's ORM
        - SQLAlchemy (本课所采用的实现)
        
2. 安装及配置
    - pip install sqlalchemy
    
3. 模型介绍

4. 新增数据
    - 新增单条记录
        - 使用 `Session.add()` 增加单条记录
        - 使用 `Session.commit()` 进行事务提交
        ```python
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
        ```
        
    - 新增多条记录
        - 调用多次 `Session.add()` 或者一次 `Session.add_all()` 来增加多条记录
        - 使用 `Session.commit()` 进行事务提交
        - 若多条记录插入不成功, 使用 `Session.rollback` 回滚
        ```python
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
        ```
    
5. 查询数据
    - 查询一条记录
        - 使用 `Session.query(类名).get()` 来获取一条记录
        ```python
        def get_one(self):
            '''获取一条记录'''
            return self.session.query(News).get(122)
        ``` 

    - 查询多条记录
        - 使用 `Session.query(类名).filter_by(过滤条件)` 来获取多条记录
        ```python
        def get_more(self):
            '''获取多条记录'''
            return self.session.query(News).filter_by(is_valid=1)
        ```

6. 修改数据
    - 修改一条记录
        - 先使用 `Session.query(类名).get()` 来获取这条记录所代表的对象
        - 修改这个对象
        - 通过 `Session.add(对象名)` 来修改这条记录
        - 通过 `Session.commit()` 进行事务提交
        ```python
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
        ```
        
    - 修改多条记录
        - 先使用 `Session.query(类名).filter_by(过滤条件)` 来获取多条记录所代表的 list
        - 遍历这个 list: 修改 list 中的每个对象, 通过 `Session.add(对象名)` 来修改记录
        - 通过 `Session.commit()` 进行事务提交
        ```python
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
        ```
    
7. 删除数据
    - 删除一条记录
        - 先使用 `Session.query(类名).get()` 来获取这条记录所代表的对象
        - 通过 `Session.delete(对象名)` 来删除这条记录
        - 通过 `Session.commit()` 进行事务提交
        ```python
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
        ```
        
    - 删除多条记录
        - 先使用 `Session.query(类名).filter_by(过滤条件)` 来获取多条记录所代表的 list
        - 遍历这个 list: 通过 `Session.delete(对象名)` 来删除记录
        - 通过 `Session.commit()` 进行事务提交
        ```python
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
        ```
        
    

## 二 Python 操作 MongoDB
## 三 Python 操作 Redis