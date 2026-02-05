from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_pessoas, verificar_token
from schemas import Pedido_schema, Item_pedido, Response_pedido_schema
from models import Pedido, Usuario, Itens_pedido
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

#Criação de uma rota de requisição
@order_router.get("/")
async def pedidos():
    """
    rota pradrão para pedidos.
    """
    return {"Teste"}

@order_router.post("/pedidos")
async def criar_pedido(pedido_schema: Pedido_schema, session: Session = Depends(pegar_pessoas)):
    novo_pedido = Pedido(usuario_id = pedido_schema.id_usuario, status = pedido_schema.status)
    session.add(novo_pedido)
    session.commit()
    return {"criado: " f"id do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_pessoas), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code = 400, detail = "Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Usuario nao verificado")
    pedido.status = "CANCELADO"
    session.commit()
    return {
    "mensagem": "Pedido cancelado",
    "numero_pedido": pedido.id
}
    
@order_router.get("/listar")
async def listar_pedidos( session: Session = Depends(pegar_pessoas), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Não tens autorização")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos:": pedidos
        }

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item(id_pedido: int, item_pedido_schema: Item_pedido, session: Session = Depends(pegar_pessoas), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=402, detail="Pedido nao existe")
    
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail= "usuario sem permissão")
    
    item_pedido = Itens_pedido(item_pedido_schema.quantidade,
                               item_pedido_schema.sabor,
                               item_pedido_schema.tamanho,
                               item_pedido_schema.preco_unitario,
                               id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    
    return{
        "Mensagem": "item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_pedido(id_item_pedido: int, 
                         session: Session = Depends(pegar_pessoas), 
                         usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(Itens_pedido).filter(Itens_pedido.id==id_item_pedido).first()
    
    if not item_pedido:
        raise HTTPException(status_code=402, detail="item no pedido não existe")
    
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido_id).first()
    
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail= "usuario sem permissão")

    session.delete(item_pedido)
    session.commit()
    
    return{
        "Mensagem": "item Removido com sucesso",
        "preço do pedido": pedido.preco,
        "pedido": pedido
    }
    
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_pessoas), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code = 400, detail = "Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Usuario nao verificado")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
    "mensagem": "Pedido finalizado",
    "numero_pedido": pedido.id
}

@order_router.get("/pedido/{id_pedido}", response_model=Response_pedido_schema)
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_pessoas), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(id_pedido==Pedido.id).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=400, detail="Usuario sem permissão")
    return pedido
    

@order_router.get("/listar/listar-usuario", response_model=List[Response_pedido_schema])
async def listar_pedidos_usuario( session: Session = Depends(pegar_pessoas), usuario: Usuario = Depends(verificar_token)):

    pedidos = session.query(Pedido).filter(Pedido.usuario_id==usuario.id).all()
    return pedidos