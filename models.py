from sqlmodel import SQLModel, Field
from typing import List
from sqlalchemy.types import TypeDecorator, Text
import json

class LectureBase(SQLModel):
    slideName: str
    zoomLink: str
    zoomPass: str
    url: str

class Lecture(LectureBase, table=True):
    id: int | None = Field(default=None, primary_key=True) 

class HomeworkBase(SQLModel):
    hwName: str
    description: str 
    dueDate: str     
    url: str

class Homework(HomeworkBase, table=True):
    id: int | None = Field(default=None, primary_key=True) 

class SlackBase(SQLModel):
    username: str = Field(description="The user who sent the message")
    content: str = Field(description="The content of the message")
    type: str = Field(description="The category the message falls under")
    isImportant: int = Field(default=0, description="Whether the message is considered important (0 for false, 1 for true)")
    forLater: int = Field(default=0, description="Whether the message should be sent for later")
    timestamp: str = Field(description="The time and date of the tweet's creation")

class Slack(SlackBase, table=True):
    id: int | None = Field(default=None, primary_key=True) 

class AttendanceBase(SQLModel):
    studentName: str
    attendance: str
    date: str

class Attendance(AttendanceBase, table=True):
    id: int | None = Field(default=None, primary_key=True) 

class MentorsBase(SQLModel):
    mentorName: str
    mentorEmail: str
    mentorPhone: str
    mentorSlack: str

class Mentors(MentorsBase, table=True):
    id: int | None = Field(default=None, primary_key=True) 


class GroupsBase(SQLModel):
    mentor1: str
    mentor2: str
    students: str # Apply the custom type here

    def get_students(self) -> list[str]:
        """Convert the comma-separated string to a list."""
        return self.students.split(",") if self.students else []

    def set_students(self, students: list[str]):
        """Convert a list of student names to a comma-separated string."""
        self.students = ",".join(students)


class Groups(GroupsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)