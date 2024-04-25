from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import uvicorn
from compressor import retrive_and_compress
import time
from crew import FactExtractionCrew

app = FastAPI()
DATABASE_URL = "sqlite:///./callcortex-cleric-test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
fact_extraction_crew = FactExtractionCrew()

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=True, index=True)
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
    ref_doc_ids = Column(String)


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

def get_facts_with_AI(question_id: int, db: Session):
    # Retrieve the question
    question = db.query(Question).filter(Question.id == question_id).first()

    if question:
        print('started processing')
        start = time.time()
        # Retrieve documents associated with the question
        documents = db.query(Document).filter(Document.question_id == question_id).all()
        # Perform any operations with the documents here
        doclist = [document.url for document in documents]
        # get compressed docs with RAG and llm_lingua
        compressed_docs = retrive_and_compress(question.question, doclist)
        end = time.time()
        print(f"context length: {len(compressed_docs)} \nTime: {end-start}")
        
        facts = fact_extraction_crew.run(question.question, compressed_docs)
        end = time.time()
        print(f'facts: \n{facts} \nType:{type(facts)} \nTime: {end-start}')
        
        ref_doc_ids = build_fact_ref(question.id, db)
        for fact in facts:
            fact_obj = Fact(question_id=question.id, fact=fact, ref_doc_ids=ref_doc_ids)
            db.add(fact_obj)

        question.status='done'
        db.commit()
        db.refresh(question)

        print('Update done')
    else:
        print('Question not found')

# func to build fact ref ids
def build_fact_ref(question_id, db):
    all_related_docs = db.query(Document).filter(Document.question_id == question_id).order_by(desc(Document.id)).all()
    curr_doc_ref = "@".join([str(doc.id) for doc in all_related_docs]+[str(question_id)])
    return curr_doc_ref

    
# POST endpoint to submit a question and documents
@app.post("/submit_question_and_documents")
async def submit_question_and_documents(data: SubmitQuestionAndDocuments, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    q_already_exists = False
    doc_already_exists = True
    # check if question exists
    #NOTE Logic can be improved with sentence transformers (intents) to compare questions but depends on scope of requirements for this app
    question = db.query(Question).filter(Question.question == data.question.lower()).first()
    # if no question add to db
    if not(question):
        question = Question(question=data.question.lower(), status="processing")
        db.add(question)
        db.commit()
        db.refresh(question)
    else:
        # else update status
        q_already_exists = True
        question.status='processing'
        db.commit()
        db.refresh(question)

    # add current docs to the question
    for document in data.documents:
        old_documents = db.query(Document).filter(Document.question_id == question.id).all()
        # Check for duplicates before adding
        if not any(doc.url == document for doc in old_documents):
            doc_already_exists = False
            db_document = Document(url=document, question_id=question.id)
            db.add(db_document)
    
    db.commit()
    # assuming the document links cant have duplicates since we have unique call logs
    if q_already_exists and doc_already_exists:
        print('fact ref already exists for same data')
        question.status = "done"
        db.commit()
        db.refresh(question)
    else:
        # Start a background task after responding to the request
        background_tasks.add_task(get_facts_with_AI, question_id=question.id, db=db)
    
    return {"message": "Submitted successfully"}

# GET endpoint to retrieve the latest question and facts
@app.get("/get_question_and_facts")
async def get_latest_question_and_facts(db: Session = Depends(get_db)):
    latest_question = db.query(Question).order_by(desc(Question.id)).first()
    if not latest_question:
        raise HTTPException(status_code=404, detail="No questions found")

    curr_doc_ref = build_fact_ref(latest_question.id, db)
    facts = db.query(Fact).filter(Fact.ref_doc_ids == curr_doc_ref).order_by(Fact.id).all()
    facts_list = [fact.fact for fact in facts]
    
    return GetQuestionAndFactsResponse(question=latest_question.question, facts=facts_list, status=latest_question.status)

@app.get("/")
def start_msg():
    return "server running!"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
