from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class LoginItem(BaseModel):
    username: str
    password: str

@app.get("/")
async def root(message:str):
    return {"message": message}


@app.post("/api/login")
async def login(loginItem:LoginItem):
    print(loginItem)