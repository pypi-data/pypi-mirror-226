## 说明
使用 .env 的数据库连接

## 用法

**`pip install myally_database`**

项目根目录创建 .env 文件
```.env
DB_USER=名
DB_PASSWORD=数据库密码
DB_HOST=ip
DB_PORT=端口
DB_DATABASE=数据库
```
调用后用法与包 SQLAlchemy 一致
```
from myally_database import database
# 获取数据库会话
session = database.get_session()
# 提交事务
session.commit()
# 关闭会话
session.close()
```