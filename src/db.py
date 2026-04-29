import sqlite3 #Modulo sqlite

def get_db(): #Funcao que conecta o banco de dados
    return sqlite3.connect("./sql/database.db")

def create_tables():
    with open("./sql/dump.sql", "r") as file: #A funcao vai abrir o arquivo
        sql = file.read() #Vai ler

    try:   #E vai tentar executar
        db = get_db() #Cria a conexão
        cursor =db.cursor() #Cria o cursor
        cursor.executescript(sql)#Executa o script
    except sqlite3.OperationalError as err: #Lanca a excessão em caso de erro
        print(err)
    finally: #Encerra
        cursor.close()




 