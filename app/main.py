from typing import List, Optional # データの型を明示する役割
# fastapiは本体。どのURLにアクセスするか決める
# httpexception エラーを適切に返すため
# status httpステータスコードを名前で指定するために必要
# Depends 依存性注入。共通処理を効率的にする。
from fastapi import FastAPI, HTTPException, status, Depends 
from pydantic import BaseModel, Field # Basemodelはデータの型定義。fieldは詳細なデータ制限を書けるために使う
from sqlalchemy.orm import Session

from db import SessionLocalm, engine, Base
from models import Todo

app = FastAPI(title="Day5 API Practice")