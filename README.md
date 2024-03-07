# Gerenciador de Recursos - Backend

Este é o repositório do backend para o Gerenciador de Recursos, um projeto desenvolvido em Python para auxiliar na gestão e monitoramento de recursos como água, energia, matéria-prima, entre outros.

## Funcionalidades Principais

1. **Login/Cadastro de Usuários**: Os usuários podem se cadastrar e fazer login para acessar as funcionalidades do sistema. As informações de usuário serão armazenadas de forma segura.

2. **Cadastro e Exibição de Recursos**: O sistema permite o cadastro e exibição de todos os recursos disponíveis para monitoramento. Isso inclui recursos como água, energia, matéria-prima, entre outros. Cada recurso será identificado por um nome único e terá suas informações associadas.

3. **Acompanhamento do Uso de Recursos**: Os usuários podem acompanhar o uso dos recursos ao longo do tempo. Isso inclui registrar informações sobre o consumo de cada recurso em determinados períodos.

4. **Definição de Metas de Gastos**: Os usuários podem estabelecer metas de gastos para cada recurso. Isso ajuda a monitorar e controlar o uso de recursos, garantindo que as metas sejam cumpridas.

5. **Geração de Relatórios**: O sistema é capaz de gerar relatórios detalhados sobre o acompanhamento do uso de recursos. Esses relatórios fornecem insights valiosos sobre o consumo de recursos e o desempenho em relação às metas estabelecidas.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para desenvolver a API backend.
- **Flask**: Framework web utilizado para criar a API RESTful.
- **MySQL**: Banco de dados relacional utilizado para armazenar os dados do sistema.
- **SQLAlchemy**: Ferramenta de mapeamento objeto-relacional (ORM) para facilitar a interação com o banco de dados MySQL.
- **JWT (JSON Web Tokens)**: Utilizado para autenticação e autorização de usuários.
- **Swagger**: Documentação interativa da API para facilitar o entendimento e utilização.

## Como Executar o Projeto

1. Clone este repositório para o seu ambiente de desenvolvimento.
2. Instale as dependências do projeto utilizando `pip install -r requirements.txt`.
3. Configure as variáveis de ambiente necessárias, como as chaves de segurança para JWT e as configurações de conexão com o banco de dados MySQL.
4. Execute o aplicativo utilizando `python app.py`.
5. Acesse a documentação interativa da API Swagger em `http://localhost:5000/docs` para entender como utilizar as rotas disponíveis.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues relatando problemas, sugerir melhorias ou enviar pull requests com novos recursos ou correções de bugs.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
