import sqlalchemy as sqlA
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()

#Criando a tabela clientes
class Cliente(Base):
    __tablename__ = "clientes"

    #Criando os atributos
    id = sqlA.Column(sqlA.Integer, primary_key=True, autoincrement=True)
    nome = sqlA.Column(sqlA.String(70), nullable=False)
    cpf = sqlA.Column(sqlA.String(9), nullable=False, unique=True)
    endereco = sqlA.Column(sqlA.String(90), nullable=False)

    conta = relationship("Conta", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Id: {self.id}, Cliente: {self.nome}, CPF: {self.cpf}, Endereço: {self.endereco}"

#Criando a tabela contas
class Conta(Base):
    __tablename__ = "contas"

    #Criando os atributos
    id = sqlA.Column(sqlA.Integer, primary_key=True, autoincrement=True)
    agencia = sqlA.Column(sqlA.String(6), nullable=False)
    conta = sqlA.Column(sqlA.String(9), nullable=False)
    tipo_conta = sqlA.Column(sqlA.String, nullable=False)
    saldo = sqlA.Column(sqlA.Float)
    id_cliente = sqlA.Column(sqlA.Integer, sqlA.ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Id da conta: {self.id}, Agência: {self.agencia}, Conta: {self.conta}, Tipo de conta: {self.tipo_conta}, Saldo: {self.saldo}"

#Criando a conexão com o banco de dados (SQLite)
engine = sqlA.create_engine("sqlite://")

#Criando as tabelas no BD
Base.metadata.create_all(engine)

#criando um inspector para recuperar informações do esquema do banco de dados
insp = sqlA.inspect(engine)

#Populando o banco de dados
with Session(engine) as session:
    cliente1 = Cliente(
        nome = 'Lucas Vilar',
        cpf = '123456789',
        endereco = 'Rua A',
        conta = [Conta(
            agencia = '000001',
            conta = '119889001',
            tipo_conta = "corrente",
            saldo = 0.0
        )]
    )

    cliente2 = Cliente(
        nome = "José da Silva",
        cpf = '987654321',
        endereco = 'Rua J',
        conta = [Conta(
            agencia = '000001',
            conta = '988001774',
            tipo_conta = "corrente",
            saldo = 0.0
        )]
    )

    cliente3 = Cliente(
        nome = 'Maria das Graças',
        cpf = '001990607',
        endereco = 'Rua M',
        conta = [Conta(
            agencia = '000001',
            conta = '099128990',
            tipo_conta = 'poupanca',
            saldo = 0.0
        )]
    )

    session.add_all([cliente1, cliente2, cliente3])
    session.commit()

    print("Usando select para selecionar um cliente com base no CPF")
    statement = sqlA.select(Cliente).where(Cliente.cpf.in_(['001990607']))
    for cliente in session.scalars(statement):
        print(cliente)

    print("\nOrdenando os clientes pelo nome de maneira alfabética:")
    statement_order_by = sqlA.select(Cliente).order_by(Cliente.nome)
    for cliente in session.scalars(statement_order_by):
        print(f"\n{cliente}")

    print("\nUsando JOIN para mostrar a informação completa:")
    statement_join = sqlA.select(Cliente.nome, Cliente.cpf, Conta.agencia, Conta.conta, Conta.saldo).join_from(Conta, Cliente)

    connection = engine.connect()
    clientes = connection.execute(statement_join).fetchall()
    for cliente in clientes:
        print(f"\n{cliente}")

    print("\nUsando a função COUNT para descobrir o número de registros na tabela cliente:")
    statement_count = sqlA.select(sqlA.func.count("*")).select_from(Cliente)
    for n_cliente in session.scalars(statement_count):
        print(f"\n{n_cliente}")