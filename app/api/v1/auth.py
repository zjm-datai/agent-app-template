from fastapi import APIRouter 

from fastapi.security import HTTPBearer

from app.services.auth_service import AccountService 

router = APIRouter() 
security = HTTPBearer() 
db_service = AccountService() 