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
        
### (四) 网易新闻实战
1. 项目概述

2. flask 入门
    - 安装
        - pip install flask
        - pip install flask-sqlalchemy
    
3. 搭建网易新闻框架
4. 新闻前台
5. 新闻数据的分页
6. 新闻数据的新增
7. 新闻数据的修改
8. 新闻数据的异步删除
        

## 二 Python 操作 MongoDB
### (一) MongoDB 数据库基础
1. MongoDB 数据库介绍
    - MongoDB 是面向文档的数据库
    
    - MongoDB 的几个概念
        - 文档
            - eg. `{"foo":3, "greeting":"Hello, world!"}`
            - 文档几个要点
                - 区分大小写
                - key唯一, 不可重复
                - 文档可嵌套
                - 键值对是有序的
                
        - 集合
            - 集合就是一组文档
            - 文档类似于关系库里的行
            - 集合类似于关系库里的表
            - 集合中的文档无需固定的结构 (与关系型数据库的区别)
            - 集合的命名规则
                - 不能是空字符串( `""` )
                - 不能包含 `\0` 字符 (空字符)
                - 不能使用 `system.` 的前缀 (系统保留)
                - 建议不包含保留字 `$`
                - 用 `.` 分割不同命名空间的子集合 (eg. blog.users, blog.posts)
                
        - 数据库
            - 多个文档组成集合, 多个集合组成数据库
            - 一个实例可以承载多个数据库
            - 每个数据库都有独立的权限
            - 保留的数据库名称不要使用 (admin, local, config)
    
2. 安装以及配置
    - 安装
        - (Install on Red Hat)[http://www.mongoing.com/docs/tutorial/install-mongodb-on-red-hat.html]
    
    - 启动
        - (Linux) sudo service mongodb start
        
    - 文档
        - (MongoDB Manual)[https://docs.mongodb.com/manual/]
        
3. 使用命令行操作数据库 (CRUD)
    - Mongo Shell
        - 连接本地数据库 `mongo`
        - 连接远程数据库 `mongo -u <user> -p <pass> --host <host> --port 28015`
        
    - Mongo Shell 常用命令
        - 显示所有数据库 `show dbs`
        - 切换数据库, 若该库不存在, 则创建它 `use 数据库名`
        
    - 新增文档 (Create)
        - MongoDB 中提供了以下方法来插入文档到一个集合：
            - db.collection.insert()
            - db.collection.insertOne() *New in version 3.2*
            - db.collection.insertMany() *New in version 3.2*
            
        - `db.collection.insert()` 向集合插入一个或多个文档. 要想插入一个文档, 传递一个文档给该方法; 要想插入多个文档, 传递文档数组给该方法
            ```
            db.users.insert(
                {
                    name: "sue",
                    age: 19,
                    status: "P"
                }
            )
            ```
            
        - `db.collection.insertOne()` 向集合插入单个文档
        
        - `db.collection.insertMany()` 向集合插入多个文档
        
    - 查询文档 (Read)
        - MongoDB 提供如下方法查询集合中的文档:
            - `db.collection.find(过滤条件, 映射)`
                - 过滤条件指明返回哪些文档
                - 查询映射指明返回匹配文档的哪些字段, 映射限制了 MongoDB 通过网络返回给客户端的数据量
                
            - `db.collection.findOne()`
        
    - 修改文档 (Update)
        - MongoDB 提供如下方法更新集合中的文档:
            - `db.collection.updateOne()`	即使可能有多个文档通过过滤条件匹配到，但是也最多也只更新一个文档
            - `db.collection.updateMany()` 更新所有通过过滤条件匹配到的文档
            - `db.collection.update(过滤条件, 替换后的文档内容)` 即使可能有多个文档通过过滤条件匹配到，但是也最多也只更新或者替换一个文档
            
    - 删除文档 (Delete)
        - MongoDB 提供如下方法删除集合中的文档:
            - `db.collection.remove(过滤条件)`
            - `db.collection.deleteOne()`
            - `db.collection.deleteMany()`
     
4. 练习任务
    - 创建一个学生信息表（至少包含：姓名，性别，成绩，年龄）
    - 写入十五条不同的数据
        ```
        db.students.insertMany(
       [{ name: "bob", age: 16, sex: "male", grade: 95},
         { name: "ahn", age: 18, sex: "female", grade: 45},
         { name: "xi", age: 15, sex: "male", grade: 75},
         { name: "bob1", age: 16, sex: "male", grade: 95},
         { name: "ahn1", age: 18, sex: "male", grade: 45},
         { name: "xi1", age: 15, sex: "female", grade: 55},
         { name: "bob2", age: 16, sex: "female", grade: 95},
         { name: "ahn2", age: 18, sex: "male", grade: 60},
         { name: "xi2", age: 15, sex: "male", grade: 75},
         { name: "bob3", age: 16, sex: "male", grade: 95},
         { name: "ahn3", age: 18, sex: "female", grade: 45},
         { name: "xi3", age: 15, sex: "male", grade: 85},
         { name: "bob4", age: 16, sex: "female", grade: 95},
         { name: "ahn4", age: 18, sex: "male", grade: 45},
         { name: "xi4", age: 15, sex: "male", grade: 75}
       ] )
        ```
        
    - 查询所有的男生数据（只需要学生的姓名和年龄）
        ```
        db.students.find({sex: 'male'}, {name: 1, age: true, _id: 0})
        ```
    
    - 查询成绩及格的学生信息（学生成绩大于或等于 60 分）
        ```
        db.students.find({grade: {'$gte': 60}})
        ```
    
    - 查询所有 18 岁的男生和 16 岁的女生的数据
        ```
        db.students.find({'$or': [{sex: 'male', age: 18}, {sex: 'female', age: 16}]})
        ```
    
    - 按照学生的年龄进行排序
        ```
        db.students.find().sort({age: 1})
        ```
    
    - 将所有的女学生年龄增加一岁
        ```
        db.students.update({sex: 'female'}, {'$inc': {age: 1}}, {multi: true})
        ```
    
5. 图形化管理工具操作

## 三 Python 操作 Redis