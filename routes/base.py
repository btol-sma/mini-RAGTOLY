from fastapi import FastAPI, APIRouter

baseRouter = APIRouter()
@baseRouter.get("/")
def welcome():
    return {
        "msg" : "hi" 
    }