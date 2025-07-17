from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Name(BaseModel):
    name: str

namesList = ["Lisa", "Mahir"]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/names")
async def names():
    return {
        "names": namesList
    }


@app.post("/names")
async def names(name: Name):
    namesList.append(name.name)
    return {
        "names": namesList
    }


@app.delete("/names/{name}")
async def names(name: str):
    namesList.remove(name)
    return {
        "names":namesList
    }