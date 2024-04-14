from typing import Optional
from sqlmodel import SQLModel, Field

# define category model
class Category(SQLModel, table=True):
    category_id : Optional[int] = Field(None, primary_key=True)
    category_name : str  # name of the category 
    category_description : str  # description of the category

# define quizlevel model with foreign key relationship to category
class QuizLevel(SQLModel, table=True):
    quiz_level_id : Optional[int] = Field(None, primary_key=True)
    quiz_level : str   # level of quiz
    category_id : int = Field(int, foreign_key="category.category_id") # foreign key relationship to Category 

# define quiz model with foreign key relationship to quizlevel
class Quiz(SQLModel, table=True):
    question_id : Optional[int] = Field(None, primary_key=True)
    question  :  str   # question for quiz
    quiz_level_id : int = Field(int, foreign_key="quizlevel.quiz_level_id")

# define choices model with foreign key relationship to quiz
class Choices(SQLModel, table=True):
    choice_id : Optional[int] = Field(None, primary_key=True)
    quiz_id : int = Field(int, foreign_key="quiz.question_id")   # foreign key relationship to Quiz  
    choice : str   # choice for the question
    status : bool = False # status of the choice (correct or incorrect)