from sqlmodel import Session, SQLModel, create_engine
from app.core.config import config
from app.db.schema import User, List, Item, ItemBatch # noqa: F401

engine = create_engine(config.DB_URL)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)