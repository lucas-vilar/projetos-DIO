import pymongo as pyM
import pprint

# Conectando e criando o banco de dados
client = pyM.MongoClient("mongodb+srv://lucasvilar12:HU7zi7ufVehol5g8@cluster0.9hi9eut.mongodb.net/?retryWrites=true&w=majority")
db = client.bank_db
collection =  db.bank

# Realizando bulk insert de docuentos
documents = [
    {
        "nome" : "Lucas Vilar",
        "cpf" : "123456789",
        "endereco" : "Rua A",
        "agencia" : "123",
        "num_conta" : "456789",
        "tipo_conta" : "corrente",
        "saldo" : 0.0
    },
    {
        "nome" : "José Silva",
        "cpf" : "987654321",
        "endereco" : "Rua B",
        "agencia" : "123",
        "num_conta" : "409089",
        "tipo_conta" : "poupanca",
        "saldo" : 500.0
    },
    {
        "nome" : "Julia Juliana",
        "cpf" : "789654123",
        "endereco" : "Rua J",
        "agencia" : "123",
        "num_conta" : "001789",
        "tipo_conta" : "corrente",
        "saldo" : 100.0
    }
]

#Inserindo os documentos no banco de dados
collection.insert_many(documents)

#Recuperando todos os registros
for document in collection.find():
    print("")
    pprint.pprint(document)

print("\nRecuperando um documento específico pelo CPF\n")
pprint.pprint(collection.find_one({"cpf" : "987654321"}))

print("\nRecuperando a quantidade de documentos no banco\n")
pprint.pprint(collection.count_documents({}))