# これから窓口とDB操作処理を分離させる。このファイルではDB操作を担う。現在はtodo.pyがどちらも兼ねている。
from __future__ import annotations # 未定義の型や循環参照を一時的に気にせずかける。

from dataclasses import dataclass
from sqlalchemy.orm import Session

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate, TodoDoneUpdate

@dataclass
class NotFoundError(Exception):
    message: str = "Resource not found"

def list_todos(db: Session) -> list[Todo]:
    return db.query(Todo).order_by(Todo.id).all()

def get_todo(db: Session, todo_id: int) -> Todo:
    row = db.query(Todo).filter(Todo.id == todo_id).first()
    if row is None: 
        raise NotFoundError("Todo not found")
    return row 

def create_todo(db: Session, payload: TodoCreate) -> Todo:
    row = Todo(title=payload.title, detail=payload.detail, done=False)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def update_todo(db: Session, todo_id: int, payload: TodoUpdate):
    row = get_todo(db, todo_id)
    
    if payload.title is not None:
        row.title = payload.title
    if payload.detail is not None:
        row.detail = payload.detail
    
    db.commit()
    db.refresh(row)
    return row

def delete_toco(db: Session, todo_id: int) -> None:
    row = get_todo(db, todo_id)
    db.delete(row)
    db.commit()

def set_done(db: Session, todo_id: int, payload: TodoDoneUpdate):
    row = get_todo(db, todo_id)
    row.done = payload.done
    db.commit()
    db.refresh(row)
    return row
