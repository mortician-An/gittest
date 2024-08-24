import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 데이터베이스 연결 및 테이블 생성
def init_db():
    print("init_db")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

    # 기본 사용자 추가
    default_users = [
        ('admin', 'admin123'),
        ('user1', 'password1')
    ]

    for username, password in default_users:
        cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", (username, password))
    print("done")
    conn.commit()
    conn.close()

# 데이터베이스에서 사용자 검증
def verify_user(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == password:
        return True
    return False

class LoginItem(BaseModel):
    username: str
    password: str

@app.get("/api/file")
async def root(message:str):
    return {"message": message}


@app.post("/api/login")
async def login(loginItem:LoginItem):
    if verify_user(loginItem.username, loginItem.password):
        return {"message": "접속되었습니다."}
    else:
        raise HTTPException(status_code=403, detail="Access forbidden: You do not have permission to access this resource.")

@app.get("/api/home")
async def home(path:str):
    print("파일이 ")


if __name__ == "__main__":
    init_db()  # 서버 시작 시 데이터베이스 초기화 및 기본 사용자 추가
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
