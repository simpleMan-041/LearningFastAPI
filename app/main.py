from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel,Field

app = FastAPI(title="Day2 API Practice")

# スキーマ
class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="短いタイトル(必須)"
        ) # Field関数はデータに制約を加える
    detail: str | None = Field(  # str | NoneはOptionalよりも型ヒントかつnullになる可能性を分かりやすく示唆できるため前者を使おう
        default=None,
        max_length=200,
        description="詳細(任意)"
        )

class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    detail: str | None = Field(default=None, max_length=200)  # Doneの状態はリスト化されたときに変更できる。編集時に変更できるのはタイトルとその詳細だけに留めるべき。

class TodoOut(BaseModel):
    id: int
    title: str
    detail: Optional[str] = None
    done: bool

# メモリ上の簡易なDBライク
todos: Dict[int,TodoOut] = {} # intとTodoOutオブジェクトの入る辞書を初期化。
next_id: int = 1 # IDの管理用変数

# @app.はどのURLにどんな方法でアクセスが来たとき、どの関数を動かすかを決める。引数は発火点といえる。
# appにはFastAPIインスタンスが入っている。FastAPIインスタンスの一員として登録すると言っている。
# @appを付けることで自動変換、型チェックを行ってくれる。
# .~~~には通信処理を行う役割がある。

@app.get("/")
def read_root():
    return {"message": "Todo APIです"}

@app.get("/health") # .getはデータの取得(検索、ページ表示)目的に
def health_check(): # システムが稼働しているかを確認する目的。シンプルな辞書データのみを返す
    return {"status": "ok"}

@app.get("/todos", response_model=List[TodoOut]) # response_modelはこの関数が返す型を自動的に右辺の型に変換する指示を出している。
def list_todos():
    return list(todos.values()) # IDを無視してvalueであるTodoOutだけを取り出し、リスト化。

@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.post("/todos", response_model=TodoOut,status_code=status.HTTP_201_CREATED) # status_codeは処理実行に対する報告。201は作成に成功したことを表す
def create_todo(payload: TodoCreate): # ユーザから送られてきたタイトルや詳細といったデータが入るTodoCreateオブジェクト引数
    global next_id # 関数の外にある変数を利用するために必要な宣言
    todo = TodoOut(id=next_id, title=payload.title,detail=payload.detail,done=False) # 新しいtodoデータ本体を作る、TodoCreateと異なる点はIDが加えられていることである。入力時点ではIDが決まっていないため、投稿の段階で付与する。
    todos[next_id] = todo # todosに整形されたデータが入る
    next_id += 1
    return todo

@app.put("/todos/{todo_id}",response_model=TodoOut) # {todo_id}はアクセスしたタスクIDが入る
def update_todo(todo_id: int, payload: TodoUpdate):
    if todo_id not in todos: # 存在しないIDを更新しようとしたとき
        raise HTTPException(status_code=404, detail="Todo not found") # データが存在しないと返す
    current = todos[todo_id]
    updated = current.model_copy( # model_copyは一部差し換える
        update={
            "title":payload.title if payload.title is not None else current.title,
            "detail":payload.detail if payload.detail is not None else current.detail,
            "done":payload.done if payload.done is not None else current.done,
            # 新しいデータがあるならそれを使い、ないならそのままで。((payload.done if payload.done is not None)else cerrent.done)とみると良いかも
        }
    )
    todos[todo_id] = updated
    return updated

@app.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int): # 引数に対応するIDのtodoを削除する。指定された引数がなければ例外を投げる。
    if todo_id not in todos: 
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return None