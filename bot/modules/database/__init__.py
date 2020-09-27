from misc import Session, Base
import functools


def db_handler(commit=False):
    '''
    Return a decorator to decorating a function 
    to use database in this function
    '''
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            session = Session()
            result = function(session, *args, **kwargs)
            if commit:
                session.commit()
            session.close()
            return result
        return wrapper
    return decorator

