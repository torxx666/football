from fastapi import FastAPI, Depends
from pymongo.database import Database
from fastapi.responses import JSONResponse
import database

from users.users_manager import UsersManager
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome"}
        
@app.get("/get_users")
def get_users(user_ids:str="", skip: int = 0, limit: int = 10):
    user_mgr = UsersManager(database.db)
    return JSONResponse(content=user_mgr.get_user_list(user_ids, skip, limit))


