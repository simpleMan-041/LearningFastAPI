# CRUD操作を提供する役割を持つファイル
from typing import List # 型ヒント
from fastapi import APIRouter, Depends, HTTPException, status # APIRouterは後で分割したファイルをまとめるために使う、Dependsは依存注入、HTTPはエラー通知機能、statusはHTTPステコを名前で指定可能にする。
from sqlalchemy.orm import Session # SessionはDB接続における設定を管理する。このファイルでは扱わないが、小文字のsessionはDB操作を行う主体。

from app.deps import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate, TodoOut

router = APIRouter(prefix="/todos", tags=["todos"]) # prefixはURLのパスに共通の文字列を付与する。tagsは自動生成ドキュメントのグループ分け。今回は全てtags。

@router.get("/{todo_id}", response_model=List[TodoOut])
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.id).all()

@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    row = db.query(Todo).filter(Todo.id == todo_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found!")
    return row

@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    row = Todo(title=payload.title, detail=payload.detail, done = False)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    row = db.query(Todo).filter(Todo.id == todo_id).first() # rowは参照でつながったオブジェクトそのもの。処理を加えなくてもrowをいじればデータも変わる。
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if payload.title is not None:
        row.title = payload.title
    if payload.detail is not None:
        row.detail = payload.detail
        
    db.commit()
    db.refresh(row)
    return row    

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    row = db.query(Todo).filter(Todo.id == todo_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(row)
    db.commit()
    return None