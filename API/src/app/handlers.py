from . import crud, schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta
import uuid
import os

def get_url_by_id(db: Session, url_id: str):
    try:
        url = crud.get_url_by_id(db, url_id)

    except HTTPException as e:
        raise e
    
    else:
        if url is None:
            raise HTTPException(status_code=404, detail="url not found")
        return url

def get_urls(db: Session):
    try:
        urls = crud.get_urls(db)

    except HTTPException as e:
        raise e
    
    else:
        if urls is None:
            raise HTTPException(status_code=404, detail="urls is empty")
        return urls

def get_url(db: Session, path: str):
    try:
        url = f"{os.getenv("DOMAIN")}/{path}"
        url = crud.get_url(db, url=url)

    except HTTPException as e:
        raise e
    
    else:
        if url is None:
            raise HTTPException(status_code=404, detail="url not found")

        if(datetime.utcnow() > url.expiration_date):
            raise HTTPException(status_code=419, detail="Page Expired")

        crud.record_visit(db, url.id)
        return url

def create_url(db: Session, create_request: schemas.URLCreate):

    prefix = f"{create_request.prefix}-" if create_request.prefix else ""
    unique_id = uuid.uuid4().hex[:8]
    
    new_url = models.URL(
        original_url= create_request.original_url,
        short_url=f"{os.getenv('DOMAIN')}/{prefix}{unique_id}",
        click_count=0,
        activation_date=datetime.utcnow(),
        expiration_date=datetime.utcnow() + timedelta(days=int(os.getenv("DELTA_TIME", 3)))
    )
    
    try:
        url = crud.create_url(db, new_url)

    except HTTPException as e:
        raise e
    
    else:
        if url is None:
            raise HTTPException(status_code=404, detail="url not found")

        elif (datetime.now() > url.expiration_date):
            raise HTTPException(status_code=419, detail="Page Expired")

        return url