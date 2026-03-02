# このファイルではバリデーションを行う。
# 新規作成、更新、表示、出力用のルールを設定。
from pydantic import BaseModel, Field, ConfigDict

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50, description="短いタイトル[必須です]")
    detail: str | None = Field(default=None, max_length=200, description="詳細を書きましょう")

class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=30)
    detail: str | None = Field(default=None, max_length=100)
    
class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    detail: str | None = None
    done: bool