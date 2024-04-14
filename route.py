from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from contextlib import asynccontextmanager
from typing import Annotated

from quiz_backend.db.db_connector import  createTable  #, get_session
from quiz_backend.models.user_models import User
from quiz_backend.utils.exception import (NotFoundException, InvalidInputException, ConflictException)
from quiz_backend.controllers.user_controllers import signUpFn

# define async context manager for appliction lifespan
@asynccontextmanager
async def life_span(app: FastAPI):
    print("Creating tables ... ")
    createTable()
    yield
    
# create FastAPI application instance with custom lifespan event handler
app = FastAPI(lifespan=life_span)

## FastAPI provide exception_handlers :- @app.exception_handler()
@app.exception_handler(NotFoundException)
def not_found(request: Request, exception: NotFoundException):
    return JSONResponse(status_code=404, content=f"{exception.not_found} ... Not Found" )

@app.exception_handler(InvalidInputException)
def invalid_input(request: Request, exception: InvalidInputException):
    return JSONResponse(status_code=422, content=f'{exception.invalid_input} ... already exist' )
    
@app.exception_handler(ConflictException) 
def conflict_input(request: Request, exception: InvalidInputException):
    return JSONResponse(status_code=400, content=f'{exception.conflict_input} ... invalide email or password')   

# define route for home endpoint
@app.get("/")
def home():
    return "Quiz Project"

@app.get("/api/get_User")
def getUser(user:str):
    if user == "akbar":
        raise NotFoundException("User")
    return "User has found ..."

@app.get("/api/input_User")
def inputUser(user: str):
    if user == "akram":
        raise InvalidInputException("User")
    return "User has found ..."

@app.get("/api/conflict_Input")
def conflict_input(user: str):
    if user == "asma":
        raise ConflictException("User")
    return "User has found ..."


# query parameter (?)
def getUser(name : str):
    return name

@app.get("/api/getUser")
def get_user(user: Annotated [str,Depends(getUser)]):
    return user

# @app.post("/api/userSignup")
# def user_signup(token_data: Annotated[object, Depends(signUpFn)]):
#     if not token_data:
#         raise NotFoundException("Token")
#     return token_data

@app.post("/api/userSignup")
def user_signup(token_data: any = Depends(signUpFn)):
    if not token_data:
        raise NotFoundException("Token")
    return token_data


