import asyncio
import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

class objeMail(BaseModel):
  correo :str
  dias: int

async def backend():
    p=subprocess.call(["python", "backend.py"],
                   stdout=subprocess.PIPE)
    
    print(p)


@app.get("/hello")

async def hello():
    await backend()
    return {"Hello world!"}  



@app.get("/correos", )  
def datos():
  datos = manipulacionArchivos.OpenfileCorreos()
  return datos;

@app.post("/agregar", )
  
async def updateCorreos(item: objeMail):  
  return manipulacionArchivos.agreeMail(item.correo,item.dias)
 
#  datos = manipulacionArchivos.upDateFileCorreos("prueba1@henry.com",0)
#   return datos