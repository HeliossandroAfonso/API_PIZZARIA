from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends,HTTPException
from models import engine, Usuario
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def pegar_pessoas():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_pessoas)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido")
    return usuario