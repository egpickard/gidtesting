from typing import Union, List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn

from model_predict import predict_from_convo, brute_predictor, online_brute_predictor
from fastapi.middleware.cors import CORSMiddleware

import os
import redis
import atexit

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect to redis server
redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379)

r.setnx("files_analyzed", 0)
r.setnx("grooming_detected", 0)
r.setnx("no_grooming_detected", 0)
r.setnx("unable_to_analyze", 0)

atexit.register(r.save)

# At startup print the values so far


def print_redis(r):
    print("Files analyzed: " + r.get("files_analyzed").decode())
    print("Number of grooming detected: " +
          r.get("grooming_detected").decode())
    print("Number of no grooming detected: " +
          r.get("no_grooming_detected").decode())
    print("Number unable to analyze: " + r.get("unable_to_analyze").decode())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class Convo(BaseModel):
    conversation: str


@app.post("/predict")
async def predict_convo(convo: Convo):
    # potentially load model here
    conversation = convo.dict()["conversation"]
    pred = predict_from_convo(conversation)
    return {"pred": pred}


@app.post("/api/online_upload")
async def upload_files(files: List[UploadFile] = File(...)):
    # handle the file upload here
    file_contents = []
    for file in files:
        # file_names.append(file.filename)
        contents = await file.read()
        # pred = predict_from_xml(contents)
        online_pred = online_brute_predictor(contents)
        print(online_pred)
        file_contents.append(
            {"name": file.filename, "online_pred": online_pred})

    return {"files": file_contents}


@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    # handle the file upload here
    file_contents = []
    for file in files:
        # file_names.append(file.filename)
        contents = await file.read()
        # pred = predict_from_xml(contents)
        pred = brute_predictor(contents, as_percent=True)
        file_contents.append(
            {"name": file.filename, "percentage": pred})
        # data storage on redis server
        r.incr("files_analyzed")
        if type(pred) == float and pred <= 0.5:
            r.incr("no_grooming_detected")
        elif type(pred) == float and pred >= 0.5:
            r.incr("grooming_detected")
        else:
            r.incr("unable_to_analyze")
        # file_contents.append(
        #     {"name": file.filename, "contents": contents.decode()})
    print_redis(r)
    return {"files": file_contents}


class Text(BaseModel):
    text: str


@app.post("/mirror")
async def mirror_string(text: Text):
    return text

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
