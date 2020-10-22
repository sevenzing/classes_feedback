from modules.common.config.constants import SERVER_API_URL
import logging
import requests
from json import loads

def get_survey(survey_pk):
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

class Survey:
    def __init__(self, survey_short_name, questions, deadline, *args, **kwargs):
        self.title = survey_short_name
        self.deadline = deadline
        self.questions = list(map(lambda data: Question(**data), questions))
        self.course = kwargs.get('course', None)
        if self.course:
            self.course = Course(**self.course)

    def __str__(self):
        return f'Survey "{self.title}" for course {self.course}\n\n' + '\n'.join(list(map(str, self.questions)))

class Question:
    def __init__(self, number, required, question_text, question_type, data, *args, **kwargs):
        self.number = number
        self.required = required
        self.text = question_text
        self.type = question_type
        self.data = data
    
    def __str__(self):
        return f'Question #{self.number} ({self.type}): "{self.text}"\n' + '\n'.join(self.data)

class Course:
    def __init__(self, subject, degree, year, *args, **kwargs):
        self.subject = subject
        self.degree = degree
        self.year = year
    
    def __str__(self):
        return f"{self.degree}-{self.year} {self.subject}"