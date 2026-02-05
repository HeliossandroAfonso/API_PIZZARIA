#Sistema para uma pizzaria
#uvicorn main:app --reload comando para executar o servidor

from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE= int(os.getenv("ACCESS_TOKEN_EXPIRE"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-from")


from order_routers import order_router
from auth_routers import auth_router

#endpoint:
#(get) dominio.com/pedidos/

#Rest APIs 
#Get -> Leitura/pegar
#Post -> adicionar/criar
#Put/Patch -> editar
#Delete -> deletar

app.include_router(order_router)
app.include_router(auth_router)