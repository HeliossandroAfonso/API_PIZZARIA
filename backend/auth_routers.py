from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_pessoas, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE, SECRET_KEY
from schemas import Usuario_schemas, Login_schema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth",tags=["auth"])

def criar_token(id_usuario, duracao_tk =timedelta(minutes=ACCESS_TOKEN_EXPIRE)):
    #JWT
    data_expiracao = datetime.now(timezone.utc) + duracao_tk
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado  

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario

#Criação de uma rota de requisição
@auth_router.get("/")
async def home():
    """
    rota padrão para autenticação.
    """
    return {"nada"}

@auth_router.post("/criar_conta")
async def criar_conta(
    usuario_schemas: Usuario_schemas,
    session: Session = Depends(pegar_pessoas)
):
    usuario = session.query(Usuario).filter(
        Usuario.email == usuario_schemas.email
    ).first()

    if usuario:
        raise HTTPException(
            status_code=400,
            detail="Usuário com este email já existe"
        )

    senha = usuario_schemas.senha[:72]
    senha_crypt = bcrypt_context.hash(senha)

    novo_usuario = Usuario(
        nome=usuario_schemas.nome,
        email=usuario_schemas.email,
        senha=senha_crypt,
        activo=usuario_schemas.activo,
        admin=usuario_schemas.admin
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return {"msg": "Usuário criado com sucesso"}

#login -> email e senha -> token JWT (Json web Token) dsfkjsdfskjfsf

@auth_router.post("/login")
async def login(login_schema: Login_schema, session: Session = Depends(pegar_pessoas)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session) 
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou Senha errada")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_tk=timedelta(days=7))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }
    
#Login para usar o fastapi
@auth_router.post("/login-from")
async def login_form(dados_from: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_pessoas)):
    usuario = autenticar_usuario(dados_from.username, dados_from.password, session) 
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou Senha errada")
    else:
        access_token = criar_token(usuario.id)
        #refresh_token = criar_token(usuario.id, duracao_tk=timedelta(days=7))
    
    return {
        "access_token": access_token,
        #"refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.get("/refresh")
async def refresh(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }