from typing import Union
from pymongo.results import UpdateResult, InsertOneResult 
from umongo import Document, fields, validate
from marshmallow.exceptions import ValidationError
from modules.database import mongo_instance
import logging


@mongo_instance.register
class User(Document):
    '''
    Represents user of bot
    '''
    chat_id = fields.IntField(required=True, unique=True)
    username = fields.StrField(required=True)
    email = fields.EmailField(required=True)


    def update(self, **attrs) -> Union[UpdateResult, InsertOneResult]:
        for attr in attrs:
            self[attr] = attrs[attr]
        return self.commit()

    class Meta:
        collection_name = 'users'

def find_user(**dct) -> User:
    '''
    Finds user in database
    '''
    return User.find_one(dct)

def create_user(chat_id, email, username) -> User:
    '''
    Creates User 
    '''
    user = User(chat_id=chat_id, email=email, username=username)
    user.commit()
    user.required_validate()
    logging.debug(f"User with params {(chat_id, email, username)} created.")
    return user

