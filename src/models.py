from typing import Optional
from dataclasses import dataclass

#Essa classe tem como objetivo, ser um modelo que vai representar 
#A entidade no banco de dados. Não é obrigatorio mas facilita a manipulacao dos dados SQL
@dataclass 
class Product:
    id: int
    name: str
    description: Optional[str]
    quantity: int
    price: float

#Essa estrutura facilita o retorno das respostas


