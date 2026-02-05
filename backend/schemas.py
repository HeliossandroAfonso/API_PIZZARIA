#Forçar tipagem de dados
from pydantic import BaseModel
from typing import Optional, List

class Usuario_schemas(BaseModel):
    nome: str
    email: str
    senha: str
    activo: Optional[bool] = True
    admin: Optional[bool] = False
    
    class Config:
        from_attributes: True
    
class Pedido_schema(BaseModel):
    id_usuario: int
    status: str

    class Config:
        from_attributes: True
        
class Login_schema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes: True
        
class Item_pedido(BaseModel):
    quantidade: int
    sabor: str 
    tamanho: str 
    preco_unitario: float
    
    class Config:
        from_attributes: True
        
class Response_pedido_schema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[Item_pedido]
    
    class Config:
        from_attributes: True
            