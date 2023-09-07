from fastapi import FastAPI, Depends
from pymongo.database import Database
import database

from users.users_manager import UsersManager
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de documentation"}
        
@app.get("/get_users")
async def get_users(skip: int = 0, limit: int = 10):

    user_mgr = UsersManager(database.db)
    return user_mgr.get_user_list(skip, limit)
    # return {"category": "ok", "documents": []}

