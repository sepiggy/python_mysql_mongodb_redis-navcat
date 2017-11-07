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
        
### (二) Python API
1. 环境配置以及依赖安装
    - python 3
    - mysql
    - pip
    - virtualenv
    - pip install mysql-client
    
2. 使用 Python 连接数据库
    ```python

    ```

3. 使用 Python 查询数据库中的数据
    - 准备 SQL
    - 找到 cursor
    - 执行 SQL
    - 拿到结果
    - 处理结果
    - 关闭 cursor / 连接
    
4. 使用 Python 新增数据到数据库
        
    

## 二 Python 操作 MongoDB
## 三 Python 操作 Redis