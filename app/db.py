from sqlalchemy import create_engine # DB接続の土台を作るためのライブラリ
from sqlalchemy.orm import sessionmaker, DeclarativeBase # sessionmakerはトランザクション管理、declaretivebaseはpythonクラスとDBテーブルのマッピング

DATABASE_URL = "sqlite:///./todo.db"
# DB接続の土台を作っている～
engine = create_engine(
    DATABASE_URL, # 第一引数にはDBのパスを入れよう
    connect_args={"check_same_thread":False}, # SQLiteにて複数のスレッド処理を行う場合はfalse。SQLiteは一つの処理しかできないのがデフォ。
)
# autocommit,Falseは命令があるまで保存はしないってこと
# autoflush,Falseは命令があるまでデータ反映はしない
# bindはどのDBに接続するかを保存
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaretivebaseを継承したクラスはDBのテーブルとして使う。
class Base(DeclarativeBase):
    pass