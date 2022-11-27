import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import manipulacionArchivos

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "chrome-extension://jlllbhmpmbjpehepminenahbjcjhmlkn"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")

def hello():
  subprocess.call("backend.py", shell=True)
  return {"Hello world!"}  


@app.get("/correos", )
  
def datos():
  datos = manipulacionArchivos.OpenfileCorreos()
  return datos;

