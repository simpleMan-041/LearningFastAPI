from sqlalchemy import String, Boolean, Text # DB側に作るデータ型の指定。strは短い。textは長い文字列で使うぞ。
from sqlalchemy.orm import Mapped, mapped_column # DB列と宣言するためのペア。mappedは型ヒント、mapped_columnはDBにおける規則設定
from app.db import Base # Baseクラスを使ってデータベースのテーブルを作るぞ

class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)