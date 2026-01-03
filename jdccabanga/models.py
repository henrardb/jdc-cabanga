from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date, time

class Lesson(BaseModel):
    # Pydantic model for a lesson
    date: Optional[str] = Field(None, description="Date of the lesson")
    hour: str = Field(..., description="Time of the lesson")
    lessonName: str = Field(..., description="Name of the lesson")
    lessonSubject: Optional[str] = Field(None, description="Subject of the lesson")
    homework: Optional[str] = Field(None, description="Explanation of the homework")
    homeworkDone: bool = Field(..., description="Boolean describing if homework has been done or not")

    # Skip other information not needed
    class Config:
        extra = "ignore"
    

class Homework(BaseModel):
    # Model describing the homework extracted and formatted
    lesson: str
    subject: str
    date: str

class EmailSummary(BaseModel):
    # Model to send a structured EmailSummary
    recipient: EmailStr = Field(..., description="Recipient of the mail") 
    summary: str = Field(..., description="Summary of the mail") 
    homework_list: List[Homework] = Field(default_factory=list, description="List of homework to be done")
