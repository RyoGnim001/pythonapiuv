from http import HTTPStatus
from apiflask import APIFlask,HTTPError
from schemas import ProductIn,ProductOut,ProductFilter
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

#Passando os parametros de ProductFilter que serão percebidos pelo query paramte
@app.input(ProductFilter, location="query", arg_name="filter")
def find_all_products(filter:dict):
    db = get_db() #Estabelece a conexão com o banco
    cursor = db.cursor() 

    #Consulta o banco de dados: Sempre descreva as colunas
    query = """
        SELECT id, name, description, quantity, price
        FROM products WHERE 1 = 1 
    """

    parameters = []

    #Se o filtro foi passado
    if filter.get("search"):
        query += " AND  name LIKE ? " #Concatene
        parameters.append(f'%{filter.get('search')}%') #Esse parâmetro será passado para a interrogracao

    if filter.get("min_price"):
        query += " AND  price >= ? " #Concatene
        parameters.append(filter.get("min_price"))

    if filter.get("max_price"):
        query += " AND  price  <= ? " #Concatene
        parameters.append(filter.get("max_price"))

    cursor.execute(query,parameters)#Executa a consulta
    rows = cursor.fetchall()#Fatchall busca a consulta

    cursor.close()
    db.close()

    #ListCoprehesion 
    #Chamamos o construtor de Product com os mesmos parâmetros na mesma ordem
    #*(args), esta pqssando a tupla como argumento da funcao de forma posicional
    #Criando uma lista de products
    products = [Product(*row) for row in rows]
    return products  

#Especificando que o o para,parmetro recebera um id que será um inteiro
@app.get("/products/<int:id>")
@app.output(ProductOut) #Convertendo o objeto para um Json
def find_products_by_id(id: int):
    db = get_db() #Estabelece a conexão com o banco
    cursor = db.cursor() 

    query = """
        SELECT id, name, description, quantity, price
        FROM products WHERE id = ?
    """
    #exeutando a consulta e passando o id como o parametro da interrogracao
    cursor.execute(query,(id,))

    #Retorna a linha com os valores correspondentes do id   
    data = cursor.fetchone()

    db.close()
    cursor.close()
    

    if data is None:
        raise HTTPError(
            message="Produto não encontrado.", status_code=HTTPStatus.NOT_FOUND
        )
    
    
    return Product(*data)




@app.post("/products")
@app.input(ProductIn)#Se quiser mudar o nome e necessario fazer , arg_name='nome'.
@app.output(ProductOut)
def create_product(json_data:dict):
    db = get_db() #Estabelece a conexão com o banco
    cursor = db.cursor() 

    #Idicando através das interrogacoes que o valor é um parêmtro que será enviado
    #Posterioramente
    query = """
        INSERT INTO products(name, description, quantity, price)
        VALUES (?, ?, ?, ?) RETURNING id
    """
    #Tupla definindo os parâmetros que serão utilizados
    #Os valores dentro da tupla, será passado para as interrogracoes
    parameters = (
        json_data.get('name'),
        json_data.get('description'),
        json_data.get('quantity'),
        json_data.get('price'),
    ) 

    #Os parametros podem ser uma lista ou tupla
    cursor.execute(query,parameters)
    id: int = cursor.fetchone()[0]

    db.commit()
    cursor.close()
    db.close()


    product = Product(id, *parameters)

    return (product, HTTPStatus.CREATED)

@app.put("/products/<int:id>")
@app.input(ProductIn)
@app.output(ProductOut)
def update_product(id: int,json_data: dict):
    db = get_db() #Estabelece a conexão com o banco
    cursor = db.cursor() 

    #Idicando através das interrogacoes que o valor é um parêmtro que será enviado
    #Posterioramente
    query = """
        UPDATE products
        SET name = ?, description = ? , quantity = ? , price = ? 
        WHERE id = ?    
    """
    #Tupla definindo os parâmetros que serão utilizados
    #Os valores dentro da tupla, será passado para as interrogracoes
    parameters = (
        json_data.get('name'),
        json_data.get('description'),
        json_data.get('quantity'),
        json_data.get('price'),
        id,
    ) 

    #Os parametros podem ser uma lista ou tupla
    cursor.execute(query,parameters)


    db.commit()
    cursor.close()
    db.close()

    print(parameters[:-1])
    product = Product(id, *parameters[:-1])
    return product




@app.delete("/products/<int:id>")
def delete_product_by_id(id: int):
    db = get_db() #Estabelece a conexão com o banco
    cursor = db.cursor() 

    query = """
        DELETE FROM products 
        WHERE id = ?
    """
    
    cursor.execute(query,(id,))

    db.commit()
    cursor.close()
    db.close()

    return {"messege": "Produto Excluido com sucesso."}


if __name__ == "__main__":
    create_tables() #Cria as tabelas caso não tenha
    app.run(debug=True) 