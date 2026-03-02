# CRUD操作を提供する役割を持つファイル
from typing import List # 型ヒント
from fastapi import APIRouter, Depends, HTTPException, status # APIRouterは後で分割したファイルをまとめるために使う、Dependsは依存注入、HTTPはエラー通知機能、statusはHTTPステコを名前で指定可能にする。
from sqlalchemy.orm import Session # SessionはDB接続における設定を管理する。このファイルでは扱わないが、小文字のsessionはDB操作を行う主体。

from app.deps import get_db
from app.schemas import TodoCreate, TodoUpdate, TodoOut, TodoDoneUpdate
from app.services import todo_service

router = APIRouter(prefix="/todos", tags=["todos"]) # prefixはURLのパスに共通の文字列を付与する。tagsは自動生成ドキュメントのグループ分け。今回は全てtags。

@router.get("", response_model=List[TodoOut])
def list_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_service.list_todos(db)

@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_service.get_todo(db, todo_id)

@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    return todo_service.create_todo(db, payload)

@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    return todo_service.update_todo(db, todo_id, payload)
    
@router.patch("/{todo_id}/done", response_model=TodoOut)
def set_done(todo_id: int, payload: TodoDoneUpdate, db: Session = Depends(get_db)):
    return todo_service.set_done(db, todo_id, payload)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_service.delete_toco(db, todo_id)
    return None
    