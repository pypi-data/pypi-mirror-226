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
