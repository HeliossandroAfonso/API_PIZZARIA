from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

#conecta do banco de dados
DATABASE_URL = "postgresql+psycopg2://openpg:jaciara2014@localhost:5432/pizzaria_teste"
engine = create_engine(DATABASE_URL, echo=True)

#cria base de dados
Base = declarative_base()

#criar as tabelas no banco
# Usuario
# Pedidos
# IntensPedido

class Usuario(Base):
    #Nome da tabela
    __tablename__ = "usuarios"
    
    #atributos da tabela
    id =  Column("id", Integer, primary_key = True, autoincrement = True)
    nome = Column("nome", String, nullable = False)
    email = Column("email", String, nullable = False) 
    senha = Column("senha", String, nullable = False)
    activo = Column("activo", Boolean, nullable= False)
    admin = Column("admin", Boolean, default = False)
    pedido = relationship("Pedido", back_populates="usuario")
    
    def __init__(self, nome, email, senha, activo = True,admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.activo = activo
        self.admin = admin
        
class Pedido(Base):
    __tablename__= "pedidos"
        
    id = Column("id", Integer, primary_key = True, autoincrement = True)
    status = Column("status", String, nullable = False)
    usuario_id = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float, nullable = False)
    itens = relationship("Itens_pedido", back_populates="pedido",cascade="all, delete")
    usuario = relationship("Usuario", back_populates="pedido")
        
    def __init__(self, status, usuario_id, preco = 0):
        self.status = status
        self.usuario_id = usuario_id
        self.preco = preco
        
    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
            
        
class Itens_pedido(Base):
    __tablename__ = "Itens_pedidos"
    
    id = Column("id", Integer, primary_key = True, autoincrement = True)
    quantidade = Column("quantidade", Integer, nullable = False)
    sabor =Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"))
    pedido = relationship("Pedido", back_populates="itens")

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido_id):
        self.quantidade = quantidade
        self.sabor = sabor 
        self.tamanho = tamanho 
        self.preco_unitario = preco_unitario
        self.pedido_id = pedido_id
        
#Comando para migracao
#alembic revision --autogenerate -m ""
#alembic upgrade head

