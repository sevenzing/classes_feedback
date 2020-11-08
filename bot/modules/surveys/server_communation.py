import logging
from json import dumps, loads

import requests
from typing import Union
from modules.common.config.constants import SERVER_API_URL
from modules.database.models import Survey


def make_request(url, data=None) -> dict:
    """
    Make post or get request to the url
    """
    post = bool(data)
    logging.info(f"Make {'post' if post else 'get'} request to server. Url: {url}")
    if post:
        # POST 
        raw_response = requests.post(url, data=dumps(data))
    else:
        # GET
        raw_response = requests.get(url)
    
    if not raw_response.ok:
        raise ValueError(f"Response from server: {raw_response.content!r}")
    
    logging.info(f"Got response from server: {raw_response.content!r}")
    response_data = loads(raw_response.content)
    return response_data

def get_survey(survey_pk) -> Union[Survey, None]:
    """
    Makes request to the server
    Return list of questions for survey with pk=survey_pk
    """
    url = f"{SERVER_API_URL}survey/{survey_pk}/"
    json_respone = make_request(url)
    return Survey(**json_respone)

def get_student(email) -> dict:
    """    
    Makes request to the server to validate user information.
    Return json response from server
    """
    url = f"{SERVER_API_URL}student/by_email/"
    data = {
        'email': email,
    }
    response = make_request(url, data)
    if 'error' in response:
        logging.warning(f"error for response {response}")
        return {}
    else:
        return response

def post_answer(question_id: int, answer_data: str):
    """
    Makes request to the server to post new answer
    Returns json repsone from server
    """
    url = f"{SERVER_API_URL}answer/"
    data = {
        'question_id': question_id,
        'answer_data': answer_data,
    }
    return make_request(url, data)