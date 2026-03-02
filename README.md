# Todo API (FastAPI + SQLite)

## 概要

FastAPI と SQLite を用いて作成したシンプルな Todo 管理APIです。

本プロジェクトでは以下を目的としました：

- FastAPIの基本理解
- CRUD実装
- Router / Service 層分離
- 例外の共通化設計
- ハッカソンを想定した軽量構成

今回は自主学習として取り組んだためデプロイしていません。次回のAPI作成で挑戦します！
---

## 使用技術

- Python 3.x
- FastAPI
- SQLite
- SQLAlchemy (2.x)
- Pydantic
- Uvicorn

---

## ディレクトリ構成

```

app/
├ main.py
├ db.py
├ models.py
├ schemas.py
├ deps.py
├ routers/
│  └ todo.py
└ services/
└ todo_service.py

````

---

## 起動方法

### 1. 仮想環境作成

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
````

## API一覧

### GET /todos

Todo一覧取得

### GET /todos/{id}

指定IDのTodo取得

### POST /todos

Todo作成

```json
{
  "title": "sample",
  "detail": "detail text"
}
```

### PUT /todos/{id}

Todo更新（title / detail）

### PATCH /todos/{id}/done

完了状態更新

```json
{
  "done": true
}
```

### DELETE /todos/{id}

Todo削除

---

## 設計方針

### Router層

* HTTP入出力の責務のみ担当

### Service層

* DB操作と業務ロジック担当
* 独自例外を定義し、FastAPI側でハンドリング

### 例外処理

* NotFoundError を共通化
* main.py に exception_handler を登録

---

## 今後の改善案

* テスト追加（pytest）
* ユーザー機能追加
* 認証機能追加
* Docker対応
