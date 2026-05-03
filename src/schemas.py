from apiflask import Schema #Importando os schemas 
from apiflask.fields import String, Integer, Float #Importando os tipos
from apiflask.validators import Length, Range #Importando validadores



class ProductIn(Schema): #classes de entrada dos valores
    name = String(required=True) #Verifica se string é valido
    #Verifica se é válido se tem a quantidade minima, e iniciara por padrão em 0
    quantity = Integer(validate=[Range(min=0)],load_default=0)
    price = Float(required=True, validate=[Range(min=0.01)])
    description = String(validate=[Length(max=255)])

class ProductOut(Schema):
    id = Integer()
    name = String()
    quantity = Integer()
    price = Float()
    description = String()

class ProductFilter(Schema):
    search = String(load_default=None)
    min_price = Float(load_default=None)
    max_price = Float(load_default=None)