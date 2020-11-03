import logging

class Survey:
    def __init__(self, *args, **kwargs):
        self.raw_data = kwargs
        self.title = kwargs['survey_short_name']
        self.is_available = kwargs['is_available']
        questions = list(map(lambda data: Question(**data), kwargs['questions']))
        
        # make sure that numbering is ok
        for number, question in enumerate(questions):
            question.number = number
            question.N = len(questions)
        
        self.questions = questions
        self.course = Course(**kwargs['course'])
        self.id = kwargs.get('id', None)

    def __str__(self):
        return f'Survey "{self.title}" for course {self.course}\n\n' + '\n'.join(list(map(str, self.questions)))

class Question:
    def __init__(self, *args, **kwargs):
        self.number = kwargs['number']
        self.required = kwargs['required']
        self.text = kwargs['question_text']
        self.type = kwargs['question_type']
        self.data = kwargs['data']
        self.id = kwargs.get('id', None)
        self.N = -1
        self.raw_data = kwargs

    @property
    def description(self):
        if self.type == 0:
            return "Choose one option"
        elif self.type == 1:
            return "Choose several options"
        elif self.type == 2:
            return "Rate from 1 to 10"
        elif self.type == 3:
            return "Write plain text"
            
    def __str__(self):
        return f'Question #{self.number + 1} "{self.text}"\n{self.description}\n\n' + \
                '\n'.join(
                    map(
                        lambda x: f"{x[0]}: {x[1]}", 
                        enumerate(self.data),
                        )
                    )

class Answer:
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data', [])
        self.raw_data = kwargs
class Course:
    def __init__(self, *args, **kwargs):
        self.subject = kwargs['subject']
        self.track = Track(**kwargs['track'])
        self.id = kwargs.get('id', None)
        self.raw_data = kwargs
    def __str__(self):
        return f"{self.track} {self.subject}"

class Track:
    def __init__(self, *args, **kwargs):
        self.degree = kwargs['degree']
        self.year = kwargs['year']
        self.id = kwargs.get('id', None)
        self.raw_data = kwargs

    def __str__(self):
        return f"{self.degree}-{self.year}"
    
    def __eq__(self, other):
        return (self.degree == other.degree) and (self.year == other.year)
