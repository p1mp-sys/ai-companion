from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./chatbot.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text)
    bot_response = Column(Text)

Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CORS
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/chat/")
async def chat(user_input: str):
    # Simple bot logic, you could replace this with actual chatbot logic
    bot_response = f"You said: {user_input}"
    # Save the conversation in the DB
    db = SessionLocal()
    conversation = Conversation(user_input=user_input, bot_response=bot_response)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    db.close()
    return {
        "user_input": user_input,
        "bot_response": bot_response,
        "conversation_id": conversation.id
    }

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: int):
    db = SessionLocal()
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    db.close()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
