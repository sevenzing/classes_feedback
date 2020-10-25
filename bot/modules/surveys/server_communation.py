from modules.common.config.constants import SERVER_API_URL
import logging
import requests
from json import loads, dumps


class Survey:
    def __init__(self, survey_short_name, questions, deadline, *args, **kwargs):
        self.title = survey_short_name
        self.deadline = deadline
        self.questions = list(map(lambda data: Question(**data), questions))
        self.course = kwargs.get('course', None)
        if self.course:
            self.course = Course(**self.course)
        self.id = kwargs.get('id', None)

    def __str__(self):
        return f'Survey "{self.title}" for course {self.course}\n\n' + '\n'.join(list(map(str, self.questions)))

class Question:
    def __init__(self, number, required, question_text, question_type, data, *args, **kwargs):
        self.number = number
        self.required = required
        self.text = question_text
        self.type = question_type
        self.data = data
        self.id = kwargs.get('id', None)
    def __str__(self):
        return f'Question #{self.number} ({self.type}): "{self.text}"\n' + '\n'.join(self.data)

class Course:
    def __init__(self, subject, track, *args, **kwargs):
        self.subject = subject
        self.track = Track(**track)
        self.id = kwargs.get('id', None)
    def __str__(self):
        return f"{self.track} {self.subject}"

class Track:
    def __init__(self, degree, year, *args, **kwargs):
        self.degree = degree
        self.year = year
        self.id = kwargs.get('id', None)

    def __str__(self):
        return f"{self.degree}-{self.year}"

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

def validate_user(email, code):
    '''
    Asks server to validate user information
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
    try:
        return response_data['confirmed']
    except KeyError:
        return False
