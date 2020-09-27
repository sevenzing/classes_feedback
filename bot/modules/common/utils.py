import datetime
import pytz

from modules.common.config import constants

def get_now() -> datetime.datetime:
    '''
    Return current date according to time zone
    '''
    return datetime.datetime.now(
        pytz.timezone(constants.TIME_ZONE)
        )
