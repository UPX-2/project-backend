from flask import Flask, jsonify, request
from database import *

class ServerApi:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.connector = MySQLConnector()

        self.connector.connect()

        @self.app.route('/')
        def index():
            return 'Sucesso'

        # COMPANIES ==========================================================================================================================

        @self.app.route('/create_company', methods=['POST'])
        def create_company():
            # Obtendo os dados do formulário enviado
            name_company = request.form.get('name_company')
            email = request.form.get('email')

            try:
                # Inserindo os dados na tabela COMPANIES
                cursor = self.connector.connection.cursor()
                query = ("INSERT INTO COMPANIES (NAME_COMPANY, EMAIL) "
                         "VALUES (%s, %s)")
                data = (name_company, email)
                cursor.execute(query, data)
                self.connector.connection.commit()
                cursor.close()
                
                return 'Empresa criada com sucesso!'
            except Exception as err:
                return f'Erro ao criar empresa: {err}'

        # USERS ==========================================================================================================================

        @self.app.route('/create_user', methods=['POST'])
        def create_user():
            # Obtendo os dados do formulário enviado
            
            company_id = request.form.get('company_id')
            complete_name = request.form.get('complete_name')
            email = request.form.get('email')
            password_hash = request.form.get('password_hash')
            access_token = request.form.get('access_token')
            refresh_token = request.form.get('refresh_token')

            try:
                # Inserindo os dados na tabela USERS
                cursor = self.connector.connection.cursor()
                query = ("INSERT INTO USERS (COMPANY_ID, COMPLETE_NAME, EMAIL, PASSWORD_HASH, ACCESS_TOKEN, REFRESH_TOKEN) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
                data = (company_id, complete_name, email, password_hash, access_token, refresh_token)
                cursor.execute(query, data)
                self.connector.connection.commit()
                cursor.close()
                
                return 'Usuário criado com sucesso!'
            except Exception  as err:
                return f'Erro ao criar usuário: {err}'

        @self.app.route('/login', methods=['POST'])
        def login():
            # Obtendo os dados do formulário enviado
            email = request.form.get('email')
            password = request.form.get('password')

            try:
                # Verificando se o usuário existe e a senha está correta
                cursor = self.connector.connection.cursor()
                query = ("SELECT * FROM USERS WHERE EMAIL = %s AND PASSWORD_HASH = %s")
                cursor.execute(query, (email, password))
                user = cursor.fetchone()
                cursor.close()

                if user:
                    return 'Login bem-sucedido!'
                else:
                    return 'Credenciais inválidas.'
            except Exception as err:
                return f'Erro ao fazer login: {err}'

    def load(self):
        self.app.run(host=self.host, port=self.port)