import mysql.connector

class MySQLConnector:
    def __init__(self):
        self.user = 'root'
        self.password = ''
        self.host = 'localhost'
        self.database = 'ECOMANAGEMENT'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database,
                raise_on_warnings=True
            )
            if self.connection.is_connected():
                print('Banco conectado')
                return self.connection
        except mysql.connector.Error as err:
            print(f'Erro ao conectar ao banco de dados: {err}')

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print('Banco desconectado')
        else:
            print('Não há conexão ativa para ser fechada.')