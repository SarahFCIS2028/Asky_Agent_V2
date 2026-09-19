from pydantic  import BaseModel

class ReadingMetrics(BaseModel):
    word_count: int
    reading_time_minutes: int 
    complexity: str

class Question(BaseModel):
    id: int
    question: str
    options: list[str]
    correct_answer: str
    explanation: str

class Quiz(BaseModel):
    questions: list[Question]

class ResultBaseModel(BaseModel):
    topic: str
    mode: str
    summary: str
    reading_metrics: ReadingMetrics
    related_topics: list[str]
    quiz: Quiz
