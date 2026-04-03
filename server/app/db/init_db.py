from db.schema import SQLModel, engine

def init_db():
    SQLModel.metadata.create_all(bind=engine)