from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import Interaction
from schemas import InteractionSchema, ChatInput
from langgraph_agent import agent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI CRM HCP Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "AI CRM Backend Running"}

@app.post("/chat")
def chat_interaction(payload: ChatInput):
    result = agent.invoke({"input": payload.text})
    return {
        "structured_data": result.get("final_output", {}),
        "missing_fields": result.get("missing_fields", [])
    }

@app.post("/log-interaction")
def save_interaction(data: InteractionSchema, db: Session = Depends(get_db)):
    new_interaction = Interaction(
        hcp_name=data.hcp_name,
        interaction_type=data.interaction_type,
        product=data.product,
        notes=data.notes,
        sentiment=data.sentiment,
        concerns=data.concerns,
        follow_up=data.follow_up
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return {
        "message": "Interaction saved successfully",
        "id": new_interaction.id
    }

@app.get("/interactions")
def get_all_interactions(db: Session = Depends(get_db)):
    interactions = db.query(Interaction).order_by(Interaction.id.desc()).all()

    return [
        {
            "id": i.id,
            "hcp_name": i.hcp_name,
            "interaction_type": i.interaction_type,
            "product": i.product,
            "notes": i.notes,
            "sentiment": i.sentiment,
            "concerns": i.concerns,
            "follow_up": i.follow_up,
            "created_at": i.created_at
        }
        for i in interactions
    ]