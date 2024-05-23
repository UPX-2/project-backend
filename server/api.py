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
                        # cursor.close()

                        token = jwt.encode(data_token, self.secret_key, algorithm='HS256')

                        query = "UPDATE USERS SET ACCESS_TOKEN = %s WHERE ID = %s"
                        params = (token, user[2])
                        
                        cursor.execute(query, params)
                        self.connector.connection.commit()

                        return jsonify({'token': token})
                    else:
                        cursor.close()
                        return jsonify({'error': 'Credenciais inválidas.'}), 401
                else:
                    cursor.close()
                    return jsonify({'error': 'Usuário não encontrado.'}), 404
            except Exception as err:
                return jsonify({'error': f'Erro ao fazer login: {err}'}), 500

        # METAS ===================================================================================================================================================
        @self.app.route('/metrics', methods=['POST'])
        def create_metrics():
            # Obtendo dados do formulário de METAS

            data = request.json
            decode_token = jwt.decode(data.get('access_token'), self.secret_key, algorithms=['HS256'])
            user_id = decode_token.get('id')
            metric_name = data.get('metric_name')
            unit_measurement = data.get('unit_measurement')

            #inserindo os dados na tabela METRICS
            try:
                cursor = self.connector.connection.cursor()
                query = ("INSERT INTO METRICS (USER_ID, METRIC_NAME, UNIT_MEASUREMENT) "
                         "VALUES (%s, %s, %s)")
                data = (user_id, metric_name, unit_measurement)
                cursor.execute(query, data)
                self.connector.connection.commit()
                cursor.close()
                resposta = {"status": "success", "metric_name": metric_name, "unit_measurement": unit_measurement}

                return jsonify(resposta)
            
            except Exception  as err:
                return jsonify({'error': f'Erro ao criar métrica: {err}'}), 500

        # Rota para obter métricas
        @self.app.route('/metrics', methods=['GET'])
        def get_metrics():
            # Obtendo o token de acesso
            access_token = request.headers.get('Authorization')
            if not access_token:
                return jsonify({'error': 'Access token não fornecido.'}), 400

            try:
                decode_token = jwt.decode(access_token, self.secret_key, algorithms=['HS256'])
                user_id = decode_token.get('id')
                cursor = self.connector.connection.cursor()
                query = "SELECT ID, METRIC_NAME, UNIT_MEASUREMENT FROM METRICS WHERE USER_ID = %s"
                cursor.execute(query, (user_id,))
                metrics = cursor.fetchall()
                cursor.close()

                # Formatando o resultado em JSON
                result = []
                for metric in metrics:
                    result.append({
                        'id': metric[0],
                        'metric_name': metric[1],
                        'unit_measurement': metric[2]
                    })
                
                return jsonify(result)
            
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expirou.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido.'}), 401
            except Exception as err:
                return jsonify({'error': f'Erro ao obter métricas: {err}'}), 500

        # REGISTROS METAS ===================================================================================================================================================
        @self.app.route('/metrics_input', methods=['POST'])
        def create_input_metric():
            data = request.json
            decode_token = jwt.decode(data.get('access_token'), self.secret_key, algorithms=['HS256'])
            user_id = decode_token.get('id')
            metric_id = data.get('metric_id')
            input_value = data.get('input_value')

            try:
                cursor = self.connector.connection.cursor()
                query = ("INSERT INTO METRICS_INPUT (USER_ID, METRIC_ID, INPUT_VALUE) "
                         "VALUES (%s, %s, %s)")
                data = (user_id, metric_id, input_value)
                cursor.execute(query, data)
                self.connector.connection.commit()
                cursor.close()
                resposta = {"status": "success"}

                return jsonify(resposta)
            
            except Exception  as err:
                return jsonify({'error': f'Erro ao criar entrada: {err}'}), 500

        # Rota para obter entradas
        @self.app.route('/metrics_input', methods=['GET'])
        def get_input_metric():
            access_token = request.headers.get('Authorization')
            if not access_token:
                return jsonify({'error': 'Access token não fornecido.'}), 400

            try:

                decode_token = jwt.decode(access_token, self.secret_key, algorithms=['HS256'])
                user_id = decode_token.get('id')
                metric_id = request.args.get('metric_id')
                if not metric_id:
                    return jsonify({'error': 'metric_id não fornecido.'}), 400

                cursor = self.connector.connection.cursor()
                query = """
                    SELECT DATE_FORMAT(CREATE_AT, '%Y-%m') AS month, SUM(INPUT_VALUE) AS total_value 
                    FROM METRICS_INPUT 
                    WHERE USER_ID = %s AND METRIC_ID = %s AND CREATE_AT >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) 
                    GROUP BY DATE_FORMAT(CREATE_AT, '%Y-%m') 
                    ORDER BY DATE_FORMAT(CREATE_AT, '%Y-%m');
                """
                cursor.execute(query, (user_id, metric_id))
                metrics = cursor.fetchall()
                cursor.close()

                # Formatando o resultado em JSON
                result = [metric[1] for metric in metrics]
                while len(result) < 6:
                    result.insert(0, "0")
                result = result[:6]

                return jsonify(result)
            
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expirou.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido.'}), 401
            except Exception as err:
                return jsonify({'error': f'Erro ao obter métricas: {err}'}), 500

    def load(self):
        self.app.run(host=self.host, port=self.port)

    def encrypt_password(self, password):
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return encrypted_password
