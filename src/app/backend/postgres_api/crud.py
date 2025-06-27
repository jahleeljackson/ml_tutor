from sqlalchemy.orm import Session 
from . import models, schemas 


def create_context(db: Session, context: schemas.ContextCreate):
    db_context = models.Conversation(
        model=context.model,
        context_text=context.context_text,
        role=context.role,
    )
    db.add(db_context)
    db.commit()
    db.refresh(db_context)
    return db_context

def get_context(db: Session):
    '''Retrieve the most recent 10 contexts for a given user ID.'''
    return db.query(models.Conversation).limit(10).all()
