import databases
import sqlalchemy


#SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./sql_app.sqlite3"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


metadata.create_all(engine)
