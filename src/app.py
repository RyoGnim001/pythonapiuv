from apiflask import APIFlask
from schemas import ProductIn,ProductOut
from models import Product

from db import get_db, create_tables #importa o banco de dados

#Variável que gerencia toda a aplicacao flask
app = APIFlask(__name__, title="Product API")
app.json.sort_keys = False #Remmove a ordenacao automatica 

#Registrando rota End points
@app.get("/")#Definindo o tipo da requisicao
def index(): #Funcao responsavel por processar a requisicao
    return "Hello world"

@app.get("/products")
#Essa parte esta falando para o código que não é apenas um produto que será
#Retornado mas sim uma lista de produto
@app.output(ProductOut(many=True))
def find_all_products():
    db = get_db() #Estabelece a conexão com o banco
    cursor = db.cursor() 

    #Consulta o banco de dados: Sempre descreva as colunas
    query = '''
        SELECT id, name, description, quantity, price
        FROM products WHERE 1 = 1 
'''
    cursor.execute(query)#Executa a consulta
    rows = cursor.fetchall()#Fatchall busca a consulta

    cursor.close()

    #ListCoprehesion 
    #Chamamos o construtor de Product com os mesmos parâmetros na mesma ordem
    #*(args), esta possando a tupla como argumento da funcao de forma posicional
    #Criando uma lista de products
    products = [Product(*row) for row in rows]
    return products  



@app.post("/products")
@app.input(ProductIn)#Se quiser mudar o nome e necessario fazer , arg_name='nome'.
@app.output(ProductOut)
def create_product(json_data:dict):
    print(json_data)
    json_data["id"] = 1
    return json_data

if __name__ == "__main__":
    create_tables() #Cria as tabelas caso não tenha
    app.run(debug=True) 