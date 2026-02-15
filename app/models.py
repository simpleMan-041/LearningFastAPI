from sqlalchemy import String, Boolean, Text # DB側に作るデータ型の指定。strは短い。textは長い文字列で使うぞ。
from sqlalchemy.orm import Mapped, mapped_column # DB列と宣言するためのペア。mappedは型ヒント、mapped_columnはDBにおける規則設定
from db import Base # Baseクラスを使ってデータベースのテーブルを作るぞ