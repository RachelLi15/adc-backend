from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Lecture
from typing import List

router = APIRouter()

# here is where you do the fastapi stuff like (chatgpt did this so prob has some errors mb):
# @router.get("/")
# async def get_lectures(session: Session = Depends(get_session)):
#     query = select(Lecture)
#     return session.exec(query).all()

# @router.post("/new", response_model=Lecture)
# async def create_lecture(lecture: Lecture, session: Session = Depends(get_session)):
#     session.add(lecture)
#     session.commit()
#     session.refresh(lecture)
#     return lecture

# @router.delete("/{lecture_id}", response_model=dict)
# def delete_lecture(lecture_id: int, session: Session = Depends(get_session)):
#     query = select(Lecture).where(Lecture.id == lecture_id)
#     lecture = session.exec(query).first()
#     if not lecture:
#         raise HTTPException(status_code=404, detail="Lecture not found")
#     session.delete(lecture)
#     session.commit()
#     return {"ok": True}