from conf.db import get_db
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response

router = APIRouter()


@router.get('/')
def get_notes(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    todoes = db.query(models.ToDoList).filter(
        models.ToDoList.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(todoes), 'todo': todoes}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.ToDoListSchema, db: Session = Depends(get_db)):
    todoes = models.ToDoList(**payload.dict())
    db.add(todoes)
    db.commit()
    db.refresh(todoes)
    return {"status": "success", "todo": todoes}


@router.put('/{todoId}')
def update_note(todoId: str, payload: schemas.ToDoListSchema, db: Session = Depends(get_db)):
    todo_query = db.query(models.ToDoList).filter(models.ToDoList.id == todoId)
    db_note = todo_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {todoId} found')
    update_data = payload.dict(exclude_unset=True)
    todo_query.filter(models.ToDoList.id == todoId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_note)
    return {"status": "success", "todo": db_note}


@router.get('/{todoId}')
def get_post(todoId: str, db: Session = Depends(get_db)):
    todo = db.query(models.ToDoList).filter(models.ToDoList.id == todoId).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {id} found")
    return {"status": "success", "todo": todo}


@router.delete('/{todoId}')
def delete_post(todoId: str, db: Session = Depends(get_db)):
    todo_query = db.query(models.ToDoList).filter(models.ToDoList.id == todoId)
    note = todo_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    todo_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)