import subprocess

from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")

def hello():
  subprocess.call("backend.py", shell=True)
  return {"Hello world!"}  



