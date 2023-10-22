import databases
import sqlalchemy

DATABASE_URL = "sqlite:///test.db"
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
database = databases.Database(
    DATABASE_URL, force_rollback=False
)
