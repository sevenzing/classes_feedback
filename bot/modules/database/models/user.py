from typing import Union
from sqlalchemy import Column, Integer, String
from modules.database import db_handler, Base
from sqlalchemy.exc import IntegrityError
import logging

class User(Base):
    __tablename__ = 'users'
    
    _id = Column(Integer, primary_key=True)
    username = Column(String(40))
    string = Column(String(500))

    def update(self, **kwargs):
        return update_user(chat_id=self._id, **kwargs)

    def __repr__(self):
       return f"User(_id={self._id}, username={self.username}, string={self.string})"
        
def __get(session, chat_id) -> User:
    session.rollback()
    return session.query(User).filter_by(_id=chat_id).first() 

@db_handler()
def get_user(session, chat_id) -> User:
    return __get(session, chat_id)

def __create(session, chat_id, **kwargs) -> None:
    user = User(_id=chat_id, **kwargs)
    session.add(user)
    session.commit()

@db_handler()
def create_user_if_not_exists(session, chat_id, **kwargs) -> User:
    try:
        __create(session, chat_id, **kwargs)
    except IntegrityError:
        # user already exists
        pass
    finally:
        return __get(session, chat_id=chat_id)


@db_handler(commit=True)
def update_user(session, chat_id, **kwargs):
    return session.query(User).filter_by(_id=chat_id).update(kwargs)
    
