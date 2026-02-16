from typing import List, Optional # データの型を明示する役割
# fastapiは本体。どのURLにアクセスするか決める
# httpexception エラーを適切に返すため
# status httpステータスコードを名前で指定するために必要
# Depends 依存性注入。共通処理を効率的にする。
from fastapi import FastAPI, HTTPException, status, Depends 
from pydantic import BaseModel, Field # Basemodelはデータの型定義。fieldは詳細なデータ制限を書けるために使う
from sqlalchemy.orm import Session

from db import SessionLocal, engine, Base
from models import Todo

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
