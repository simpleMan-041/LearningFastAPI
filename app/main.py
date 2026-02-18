from typing import List, Optional # データの型を明示する役割
# fastapiは本体。どのURLにアクセスするか決める
# httpexception エラーを適切に返すため
# status httpステータスコードを名前で指定するために必要
# Depends 依存性注入。共通処理を効率的にする。
from fastapi import FastAPI, HTTPException, status, Depends 
from pydantic import BaseModel, Field # Basemodelはデータの型定義。fieldは詳細なデータ制限を書けるために使う
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine, Base
from app.models import Todo

app = FastAPI(title="Day5 API Practice")

Base.metadata.create_all(bind=engine) # baseクラスのmetadataはテーブル定義管理カタログ。createall(接続先指定)でテーブルを一斉に作成。

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoCreate(BaseModel): # BaseModelの継承により型チェックと変換、エラー、JSON変換が出来るようになる
    title: str = Field(..., min_length=1, max_length=50, description="短いタイトル[必須]") # ...はnullによりエラーを吐く
    detail: str | None = Field(default=None, max_length=200, description="詳細[任意]")

class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1,max_length=50)
    detail: str | None = Field(default=None, max_length=200)

class TodoOut(BaseModel):
    id: int 
    title: str
    detail : str | None = None
    done : bool 

@app.get("/")
def read_root():
    return {"message": "TodoAPIです"}

@app.get("/health")
def health_check():
    return {"status" : "ok"}

@app.get("/todos", response_model=List[TodoOut]) # response_modelはデータのフィルタリング、変換、ドキュメントへの反映を行う。
def list_todos(db:Session = Depends(get_db)): # dbはSession型の入る変数であり、get_dbがyieldで一時的に渡したオブジェクトが入る。
    rows = db.query(Todo).order_by(Todo.id).all() # todoテーブルデータを全て取得。idの小さい順に整列、.allでlist形式で渡す。
    return [TodoOut(id=r.id, title=r.title, detail=r.detail, done=r.done) for r in rows] # DB専用の重いormモデル(Todo)を通信専用の軽いpydanticモデル(TodoOut)に詰め替え。

@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id :int, db:Session = Depends(get_db)):
    row = db.query(Todo).filter(Todo.id == todo_id).first() # .filter(条件).first()は条件に適合する最初の一つを返す
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoOut(id=row.id, title=row.title, detail=row.detail, done=row.done)

@app.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)): # payloadはユーザーが送ってきたデータを示す。fastapiではjsonデータを指す。
    row = Todo(title=payload.title, detail=payload.detail, done=False)
    db.add(row) # git add 保存対象としてスタンバイ
    db.commit() # git commit 変更を確定。
    db.refresh(row)
    
    return TodoOut(id=row.id, title=row.title, detail=row.detail, done=row.done)