# pymysql-extension

**`Author: Joker-desire`**

pymysql-extension是一个基于pymysql的扩展，主要是为了解决pymysql在使用过程中的一些不便之处。

_**注：只用到了pymysql库，所以不用担心兼容性问题。**_

## 实现的功能

- [X] 1.SQL阅读器
- [x] 2.SQL结果对象转换器

## 安装

```shell
pip install pymysql-extension
```

## 注意事项

### 1. SQL阅读器使用时SQL文件路径设置

#### 方式一：设置SQL文件路径环境变量

```shell
export SQL_PATH=/path/to/sql
```

#### 方式二：在代码中设置SQL文件路径

```python
os.environ["SQL_PATH"] = "/path/to/sql"
```

##### 方式三：不想设置环境变量，可直接在代码中设置SQL文件路径

```python
sql = SqlReader.reader("/path/to/sql/example.sql")
```

### 2. SQL结果对象转换器使用时数据库连接配置

#### 数据库配置（默认）

```json
{
  "host": "localhost",
  "port": 3306,
  "user": "root",
  "password": "root",
  "db": "",
  "charset": "utf8"
}
```

#### 自定义配置

##### 方式一：

```python
conf = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "db": "test",
}
converter = SqlObjectConverter(**conf)
```

##### 方式二：

```python
converter = SqlObjectConverter(host="localhost", user="root", password="root", db="test")
```

## 示例

```python
from extension._sql_reader import SqlReader
from extension._sql_object_converter import SqlObjectConverter

if __name__ == '__main__':
    sql = SqlReader.reader("example.sql", user_name="Joker-desire")
    print(sql)
    # 创建SQL对象转换器
    converter = SqlObjectConverter()
    # 执行SQL,并获取结果
    results = converter.exec(sql).fetch_all()
    print(results)
    # 执行SQL,并获取结果
    result = converter.exec(sql).fetch_one()
    # 将结果转换成字典
    print(result.to_dict())
```