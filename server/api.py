from flask import Flask, jsonify, request
from flask_cors import CORS
from database import *
import bcrypt
import jwt

class ServerApi:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)  # Permitindo solicitações de qualquer origem
        self.connector = MySQLConnector()
        self.connector.connect()
        self.secret_key = 'e6b8e25c0e90427bbf52b9adfd007c0979fa59387d2de55d486d32550a815e6c'

        @self.app.route('/')
        def index():
            return 'Sucesso'

        # USERS ==========================================================================================================================

        @self.app.route('/create_user', methods=['POST'])
        def create_user():
            # Obtendo os dados enviados como JSON
            data = request.json
            complete_name = data.get('complete_name')
            email = data.get('email')
            password_hash = data.get('password')
            password_hash = self.encrypt_password(password_hash)
            access_token = ""

            try:
                # Inserindo os dados na tabela USERS
                cursor = self.connector.connection.cursor()
                query = ("INSERT INTO USERS (COMPLETE_NAME, EMAIL, PASSWORD_HASH, ACCESS_TOKEN) "
                         "VALUES (%s, %s, %s, %s)")
                data = (complete_name, email, password_hash, access_token)
                cursor.execute(query, data)
                self.connector.connection.commit()
                cursor.close()
                
                return jsonify({'return': 'success'})
            except Exception  as err:
                return f'Erro ao criar usuário: {err}'

        @self.app.route('/login', methods=['POST'])
        def login():
            # Obtendo os dados enviados como JSON
            data = request.json
            email = data.get('email')
            password = data.get('password')

            try:
                # Obtendo os dados do usuário do banco de dados
                cursor = self.connector.connection.cursor()
                query = "SELECT EMAIL, PASSWORD_HASH, ID, COMPLETE_NAME FROM USERS WHERE EMAIL = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if user:
                    # Obtendo a senha criptografada armazenada no banco de dados
                    senha_criptografada_armazenada = user[1]

                    # Verificando se a senha fornecida corresponde à senha criptografada armazenada
                    if bcrypt.checkpw(password.encode('utf-8'), senha_criptografada_armazenada.encode('utf-8')):
                        data_token = {
                            'id': user[2],
                            'email': user[0],
                            'nome_completo': user[3],
                        }
                        cursor.close()

                        token = jwt.encode(data_token, self.secret_key, algorithm='HS256')
                        return jsonify({'token': token})
                    else:
                        cursor.close()
                        return jsonify({'error': 'Credenciais inválidas.'}), 401
                else:
                    cursor.close()
                    return jsonify({'error': 'Usuário não encontrado.'}), 404
            except Exception as err:
                return jsonify({'error': f'Erro ao fazer login: {err}'}), 500

    def load(self):
        self.app.run(host=self.host, port=self.port)

    def encrypt_password(self, password):
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return encrypted_password
