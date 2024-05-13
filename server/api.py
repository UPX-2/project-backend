from flask import Flask, jsonify, request
from flask_cors import CORS
from database import *
import bcrypt

class ServerApi:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)  # Permitindo solicitações de qualquer origem
        self.connector = MySQLConnector()

        self.connector.connect()

        @self.app.route('/')
        def index():
            return 'Sucesso'

        # USERS ==========================================================================================================================

        @self.app.route('/create_user', methods=['POST'])
        def create_user():
            # Obtendo os dados do formulário enviado
            
            complete_name = request.form.get('complete_name')
            email = request.form.get('email')
            password_hash = request.form.get('password')
            password_hash = self.encrypt_password(password_hash)
            access_token = request.form.get('access_token')
            refresh_token = request.form.get('refresh_token')

            try:
                # Inserindo os dados na tabela USERS
                cursor = self.connector.connection.cursor()
                query = ("INSERT INTO USERS (COMPLETE_NAME, EMAIL, PASSWORD_HASH, ACCESS_TOKEN, REFRESH_TOKEN) "
                         "VALUES (%s, %s, %s, %s, %s)")
                data = (complete_name, email, password_hash, access_token, refresh_token)
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
                # Obtendo os dados do usuário do banco de dados
                cursor = self.connector.connection.cursor()
                query = ("SELECT EMAIL, PASSWORD_HASH FROM USERS WHERE EMAIL = %s")
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if user:
                    # Obtendo a senha criptografada armazenada no banco de dados
                    senha_criptografada_armazenada = user[1]
                    
                    # Verificando se a senha fornecida corresponde à senha criptografada armazenada
                    if bcrypt.checkpw(password.encode('utf-8'), senha_criptografada_armazenada.encode('utf-8')):
                        cursor.close()
                        return 'Login bem-sucedido!'
                    else:
                        cursor.close()
                        return 'Credenciais inválidas.'
                else:
                    cursor.close()
                    return 'Usuário não encontrado.'
            except Exception as err:
                return f'Erro ao fazer login: {err}'

    def load(self):
        self.app.run(host=self.host, port=self.port)

    def encrypt_password(self, password):
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return encrypted_password