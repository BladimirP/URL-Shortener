from sqlalchemy.orm import Session
from . import models, schemas

def get_url_by_id(db: Session, url_id: str):
    return db.query(models.URL).filter(models.URL.id == url_id).first()

def get_urls(db: Session):
    return db.query(models.URL).all()

def get_url(db: Session, url: str):
    return db.query(models.URL).filter(models.URL.short_url == url).first()

def record_visit(db: Session, url_id: int):
    url_entry = db.query(models.URL).filter(models.URL.id == url_id).first()
    url_entry.click_count += 1
    db.commit()

def create_url(db: Session, url):
    db.add(url)
    db.commit()
    db.refresh(url)
    return url