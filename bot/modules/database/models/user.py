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
    track = fields.DictField()
    current_survey = fields.DictField(default={})
    current_question = fields.DictField(default={})

    def update(self, **attrs) -> Union[UpdateResult, InsertOneResult]:
        for attr in attrs:
            self[attr] = attrs[attr]
        return self.commit()

    def __str__(self):
        return f"User({self.email})"

    class Meta:
        collection_name = 'users'

def find_user(**dct) -> User:
    '''
    Finds user in database
    '''
    return User.find_one(dct)

def create_user(chat_id, email, username, track) -> User:
    '''
    Creates User 
    '''
    user = User(chat_id=chat_id, email=email, username=username, track=track)
    user.commit()
    user.required_validate()
    logging.debug(f"User with params {(chat_id, email, username, track)} created.")
    return user

