import logging
from json import dumps, loads

import requests
from modules.common.config.constants import SERVER_API_URL
from modules.database.models import Survey


def get_survey(survey_pk) -> Survey:
    """
    Return list of questions for survey with pk=survey_pk
    """
    url = f"{SERVER_API_URL}survey/{survey_pk}/"
    logging.info(f"Make request to server. Url: {url}")
    data = requests.get(url)

    if data:
        logging.info(f"Got data: {data.content}")
        json_respone = loads(data.content)
        return Survey(**json_respone)
    else:
        logging.warning("No data got from server")


def validate_user(email, code) -> dict:
    '''
    Asks server to validate user information.
    Return json response from server
    '''
    url = f"{SERVER_API_URL}user/validate/"
    logging.info(f"Make request to server. Url: {url}")
    data = {
        'email': email,
        'code': code,
    }
    raw_response = requests.get(url, data=dumps(data))
    logging.info(f"Got response from server: {raw_response.content}")
    response_data = loads(raw_response.content)

    return response_data
