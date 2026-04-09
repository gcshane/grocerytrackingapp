from app.db.schema import User
from sqlmodel import select
from app.dependencies import SessionDep

def get_user_by_username(username: str, session: SessionDep):
    user = session.exec(select(User).where(User.username == username)).first()
    return user

def get_user_by_id(user_id: int, session: SessionDep):
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    return user