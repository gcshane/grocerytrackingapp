from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date
from core.config import config

engine = create_engine(config.DB_URL)
# session = sessionmaker(bind=engine)

class User(SQLModel, table=True):
    user_id : int | None = Field(default=None, primary_key=True)
    name : str
    email : str
    password : str
    alert : bool

class List(SQLModel, table=True):
    list_id : int | None = Field(default=None, primary_key=True)
    list_name : str
    user_id : int = Field(foreign_key="user.user_id")

class Item(SQLModel, table=True):
    item_id : int | None = Field(default=None, primary_key=True)
    item_name : str
    list_id : int = Field(foreign_key="list.list_id")
    total_quantity : int
    quantity_limit : int
    alert_days_limit : int  

class ItemBatch(SQLModel, table=True):
    expiry_date : date = Field(primary_key=True)
    item_id : int = Field(foreign_key="item.item_id", primary_key=True)
    quantity : int