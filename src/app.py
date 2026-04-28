from apiflask import APIFlask
from schemas import ProductIn
from schemas import ProductOut

#Variável que gerencia toda a aplicacao flask
app = APIFlask(__name__, title='Product API')
app.json.sort_keys = False #Remmove a ordenacao automatica 

#Registrando rota End points
@app.get('/')#Definindo o tipo da requisicao
def index(): #Funcao responsavel por processar a requisicao
    return "Hello world"

@app.post('/products')
@app.input(ProductIn)#Se quiser mudar o nome e necessario fazer , arg_name='nome'.
@app.output(ProductOut)
def create_product(json_data:dict):
    print(json_data)
    json_data['id'] = 1
    return json_data

if __name__ == '__main__':
    app.run(debug=True) 