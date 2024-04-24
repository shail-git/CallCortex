from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import uvicorn
import time  # for simulating background task

app = FastAPI()
DATABASE_URL = "sqlite:///./callcortex-cleric-test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=False, index=True)
    status = Column(String)

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))

class Fact(Base):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True, index=True)
    fact = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class SubmitQuestionAndDocuments(BaseModel):
    question: str
    documents: List[str]

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: List[str] = None
    status: str

# Simulated background task
def background_process(question_id: int, db: Session):
    time.sleep(8)  # Simulating some processing time
    # Update question status or perform any other database operation here
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        question.status = "done"
        db.commit()
    print('update done')

# POST endpoint to submit a question and documents
@app.post("/submit_question_and_documents")
async def submit_question_and_documents(data: SubmitQuestionAndDocuments, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    question = Question(question=data.question, status="processing")
    db.add(question)
    db.commit()
    db.refresh(question)

    for document in data.documents:
        db_document = Document(url=document, question_id=question.id)
        db.add(db_document)
    
    db.commit()

    # Start a background task after responding to the request
    background_tasks.add_task(background_process, question_id=question.id, db=db)
    
    return {"message": "Submitted successfully"}

# GET endpoint to retrieve the latest question and facts
@app.get("/get_latest_question_and_facts")
async def get_latest_question_and_facts(db: Session = Depends(get_db)):
    latest_question = db.query(Question).order_by(desc(Question.id)).first()
    if not latest_question:
        raise HTTPException(status_code=404, detail="No questions found")

    facts = db.query(Fact).filter(Fact.question_id == latest_question.id).all()
    facts_list = [fact.fact for fact in facts]
    
    return GetQuestionAndFactsResponse(question=latest_question.question, facts=facts_list, status=latest_question.status)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
