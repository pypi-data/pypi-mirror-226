## 说明
简单的数据库连接

## 用法

**`pip install myally_database`**

推荐搭配包 python-decouple 以便可以直接在 .env 中写配置

创建个 database.py

**`pip install python-decouple`**

```python
from decouple import config
from myally_database import Database
db_config = {
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'port': config('DB_PORT', default=3306, cast=int),
    'database': config('DB_DATABASE')
}
# 创建一个全局的Database实例，可以在其他文件中直接使用
database = Database(db_config)
```

.env 配置
```.env
DB_USER=名
DB_PASSWORD=数据库密码
DB_HOST=ip
DB_PORT=端口
DB_DATABASE=数据库
```

调用后用法与包 SQLAlchemy 一致
```
from database import database
# 获取数据库会话
session = database.get_session()
# 提交事务
session.commit()
# 关闭会话
session.close()
```