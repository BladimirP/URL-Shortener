from . import schemas, handlers, database
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import logging

##################### LOGGING ####################
logger = logging.getLogger("api_url_shortener")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("./API/src/logs/log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

################### END POINTS ###################
router = APIRouter()

@router.get("/")
async def read_root():
    """
    Root endpoint to verify that the API is online.
    
    Returns:
        str: A simple confirmation message.
    """
    return "url shortener"


@router.get("/url/{url_id}", response_model=schemas.URLResponse)
async def read_url(url_id: str, request: Request, db: Session = Depends(database.get_db)):
    """
    Retrieve a shortened URL record by its unique ID.

    Args:
        url_id (str): The ID of the URL record.
        request (Request): The incoming request object for logging purposes.
        db (Session): Database session dependency.

    Returns:
        URLResponse: The data associated with the shortened URL.
    """
    try:
        response = handlers.get_url_by_id(db, url_id)
    except HTTPException as e:
        logger.error(f"GET ../url/{url_id}, FROM: {request.client.host}, STATUS: {e.status_code}")
        raise e
    else:
        logger.info(f"GET ../url/{url_id}, FROM: {request.client.host}, STATUS: 200")
        return response


@router.get("/urls", response_model=List[schemas.URLResponse])
async def read_urls(request: Request, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of all shortened URLs.

    Args:
        request (Request): The incoming request object for logging purposes.
        db (Session): Database session dependency.

    Returns:
        List[URLResponse]: A list of all shortened URLs in the system.
    """
    try:
        response = handlers.get_urls(db)
    except HTTPException as e:
        logger.error(f"GET ../urls, FROM: {request.client.host}, STATUS: {e.status_code}")
        raise e
    else:
        logger.info(f"GET ../urls, FROM: {request.client.host}, STATUS: 200")
        return response


@router.get("/{path}")
async def read_url_path(path: str, request: Request, db: Session = Depends(database.get_db)):
    """
    Redirect the user to the original URL based on the shortened path.

    Args:
        path (str): The short path of the URL.
        request (Request): The incoming request object for logging.
        db (Session): Database session dependency.

    Returns:
        RedirectResponse: A redirect response to the original URL.
    """
    try:
        response = handlers.get_url(db, path)
    except HTTPException as e:
        logger.error(f"GET ../{path}, FROM: {request.client.host}, STATUS: {e.status_code}")

        if e.status_code == 419:
            html_content = """
            <html>
                <head>
                    <title>Error 419</title>
                    <style>
                        body {
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            font-family: Arial, sans-serif;
                            background-color: #f9f9f9;
                        }
                        .container {
                            text-align: center;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Error 419 - Page Expired</h1>
                        <p>Your link has expired and is no longer valid.</p>
                    </div>
                </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=419)
        raise e
    else:
        logger.info(f"GET ../{path}, FROM: {request.client.host}, STATUS: 200")
        return RedirectResponse(url=response.original_url)


@router.post("/url", response_model=schemas.URLResponse)
async def create_url(create_request: schemas.URLCreate, request: Request, db: Session = Depends(database.get_db)):
    """
    Create a new shortened URL.

    Args:
        create_request (URLCreate): The data for the new URL to shorten.
        request (Request): The incoming request object for logging.
        db (Session): Database session dependency.

    Returns:
        URLResponse: The newly created shortened URL record.
    """
    try:
        response = handlers.create_url(db, create_request)
    except HTTPException as e:
        logger.error(f"POST ../url, FROM: {request.client.host}, STATUS: {e.status_code}")
        raise e
    else:
        logger.info(f"POST ../url, FROM: {request.client.host}, STATUS: 200")
        return response