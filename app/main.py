from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    age: int
    name: str

app = FastAPI()

@app.get("/")
async def health():
    return {"message": "Ping successfull"}

@app.get("/api/v1/hello")
async def hello_name_via_query(name: str, age: int):
    return {"message": f"Hello {name}, you are {age} years old"}

@app.get("/api/v1/hello/{name}/{age}")
async def hello_name_via_path(name: str, age: int):
    return {"message": f"Hello {name}, you are {age} years old"}

@app.post("/api/v1/hello")
async def hello_name(user: User):
    return {"message": f"Hello {user.name}, you are {user.age} years old"}

@app.put("/api/v1/update")
async def user_update(user: User):
    user.age += 1
    return {"message": f"Recurso atualizado com o nome: {user.name}, idade {user.age}"}

@app.delete("/api/v1/delete")
async def delete_user_by_name(name: str, age: int):
    return {"message": f"Recurso deletado com o nome: {name}, idade {age}"}

@app.patch("/api/v1/patch")
async def patch_user(user: User):
    return {"message": f"Modificação parcial aplicada ao recurso com o nome: {user.name}, idade {user.age}"}