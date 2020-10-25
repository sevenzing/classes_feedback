
class Survey:
    def __init__(self, *args, **kwargs):
        self.raw_data = kwargs
        self.title = kwargs['survey_short_name']
        self.is_available = kwargs['is_available']
        self.questions = list(map(lambda data: Question(**data), kwargs['questions']))
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
        self.raw_data = kwargs

    def __str__(self):
        return f'Question #{self.number} ({self.type}): "{self.text}"\n' + '\n'.join(self.data)

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
