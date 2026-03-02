# このファイルはDBとの安全な通信チャンネルを必要な時だけ貸し出す管理者。
# 必要な時だけDBを呼びだし、セッションを必ず閉じる。また、依存注入の準備段階でもある。
from typing import Generator
from sqlalchemy.orm import Session
from app.db import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal() # SessionLocal()を通して生まれたdbオブジェクトはDBとの接続におけるパイプラインとなる。ただ、db変数自体は接続システムを操作するリモコンに過ぎない。
    try:
        yield db 
    finally:
        db.close()