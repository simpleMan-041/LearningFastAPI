from fastapi import FastAPI
from app.db import Base, engine
from app.routers.todo import router as todo_router

app = FastAPI(title="API Practice")

Base.metadata.create_all(bind=engine) # Baseはテーブル定義、metadataはカラム情報、create_all(bind=engine)は接続先情報(engine)へテーブルを全部作れ命令。

@app.get("/")
def read_root():
    return {"message": "TodoAPI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(todo_router) # 別ファイルで小分けに作った機能を集結させる！ここに集え、我らが同胞よ！