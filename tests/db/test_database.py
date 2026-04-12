from sqlalchemy import inspect
from unittest.mock import patch
from sqlmodel import create_engine, Session, select

from app.db.database import init_db
from app.db.schema import User

def test_init_db_physically_creates_tables():
    test_engine = create_engine("sqlite:///:memory:")
    
    with patch("app.db.database.engine", test_engine):
        
        init_db()
        
        inspector = inspect(test_engine)
        actual_tables = inspector.get_table_names()
        
        assert "user" in actual_tables
        assert "list" in actual_tables
        assert "item" in actual_tables
        assert "itembatch" in actual_tables

        with Session(test_engine) as session:
            fake_user = User(
                username="test_sqlite_user", 
                name="Test", 
                email="test@test.com", 
                password="hashed", 
                alert=True
            )
            session.add(fake_user)
            session.commit()
            
            retrieved_user = session.exec(select(User)).first()
            
            assert retrieved_user.username == "test_sqlite_user"