from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = self._create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def _create_engine(self):
        db_url = f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        return create_engine(db_url)

    def get_session(self):
        return self.Session()


# 数据库配置
db_config = {
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'port': config('DB_PORT', default=3306, cast=int),
    'database': config('DB_DATABASE')
}


# 创建一个全局的Database实例，可以在其他文件中直接使用
database = Database(db_config)
