from fastapi import FastAPI
from pydantic import BaseModel
from fileUpload import file_router

app = FastAPI()
app.include_router(file_router, prefix="/files", tags={"files"})

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