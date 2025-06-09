from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import os
import shutil
import uuid

from database import Base, Card as DBCard, engine, SessionLocal

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Card(BaseModel):
    id: str
    name: str
    barcode: str
    image: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/cards", response_model=List[Card])
def get_cards(db: Session = Depends(get_db)):
    return db.query(DBCard).all()

@app.post("/api/cards", response_model=Card)
def create_card(
    name: str = Form(...),
    barcode: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    id = str(uuid.uuid4())
    image_path = f"{UPLOAD_DIR}/{id}_{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    card = DBCard(id=id, name=name, barcode=barcode, image=os.path.basename(image_path))
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@app.delete("/api/cards/{card_id}")
def delete_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(DBCard).filter(DBCard.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
    return {"status": "deleted"}

@app.get("/uploads/{filename}")
def get_image(filename: str):
    return FileResponse(f"{UPLOAD_DIR}/{filename}")
