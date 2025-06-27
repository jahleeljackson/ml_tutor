from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from postgres_api import schemas, crud
from postgres_api.database import get_db

router = APIRouter(prefix="/context", tags=["context"])

# Define the endpoint for creating context
@router.post('/', response_model=schemas.ContextCreate)
def create_context(
    context: schemas.ContextCreate,
    db: Session = Depends(get_db)
):
    return crud.create_context(db=db, context=context)


# Define the endpoint for retrieving all contexts
@router.get('/', response_model=list[schemas.Context])
def get_last_ten_contexts(db: Session = Depends(get_db)):
    contexts = crud.get_context(db=db)
    if not contexts:
        raise HTTPException(status_code=404, detail="No contexts found")
    return contexts