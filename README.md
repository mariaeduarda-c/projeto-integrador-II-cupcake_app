# Cupcake App

Este é um aplicativo de e-commerce de cupcakes que permite aos usuários navegar por produtos, adicionar itens ao carrinho, realizar compras (após cadastro) e gerenciar produtos e usuários através de um painel de administração.

## Tecnologias Utilizadas

**Front-end:**
*   HTML5
*   CSS3
*   JavaScript

**Back-end:**
*   Python 3
*   Flask (microframework web)
*   SQLite (banco de dados simples para este exemplo)
*   Padrão de Design MVC (Model-View-Controller)

## Estrutura do Projeto

O projeto é dividido em `frontend` e `backend`.

### `frontend/`

Contém todos os arquivos da interface do usuário:
*   `css/`: Arquivos CSS para estilização.
*   `js/`: Arquivos JavaScript para interatividade.
*   `.html`: Páginas HTML.

### `backend/`

Contém a lógica do servidor, implementada em Python com Flask:
*   `controllers/`: Lógica de requisições e respostas, intermediando Model e View.
*   `models/`: Representação dos dados e lógica de negócios.
*   `views/`: Formatação das respostas (neste caso, JSON para a API).
*   `services/`: Lógica de negócios específica que pode ser reutilizada entre controllers (ex: autenticação).
*   `tests/`: Testes unitários para o back-end.
*   `app.py`: Ponto de entrada da aplicação Flask.
*   `database.py`: Gerenciamento da conexão com o banco de dados.

## Como Executar

### Pré-requisitos

*   Python 3.x
*   pip (gerenciador de pacotes Python)

### Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/cupcake_app.git
    cd cupcake_app
    ```

2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as dependências do back-end:
    ```bash
    pip install Flask Flask-SQLAlchemy Werkzeug
    ```

### Executando o Back-end

1.  Navegue até a pasta `backend`:
    ```bash
    cd backend
    ```

2.  Execute o arquivo `app.py`:
    ```bash
    python app.py
    ```
    O servidor estará rodando em `http://127.0.0.1:5000`.

### Abrindo o Front-end

Abra os arquivos HTML diretamente no seu navegador. O JavaScript fará requisições para o back-end rodando em `http://127.0.0.1:5000`.

## Testes

Para executar os testes do back-end:

1.  Navegue até a pasta `backend/tests`:
    ```bash
    cd backend/tests
    ```

2.  Execute os testes usando `pytest` (instale-o se ainda não tiver: `pip install pytest`):
    ```bash
    pytest
    ```

## Endpoints da API (Back-end)

### Autenticação
*   `POST /api/register`: Registra um novo usuário.
*   `POST /api/login`: Autentica um usuário.

### Produtos
*   `GET /api/products`: Obtém todos os produtos.
*   `GET /api/products/<id>`: Obtém um produto específico.

### Administração
*   `POST /api/admin/products`: Adiciona um novo produto (apenas admin).
*   `PUT /api/admin/products/<id>`: Atualiza um produto existente (apenas admin).
*   `DELETE /api/admin/products/<id>`: Deleta um produto (apenas admin).
*   `GET /api/admin/users`: Lista todos os usuários (apenas admin).
*   `PUT /api/admin/users/<id>/role`: Atualiza a função de um usuário (apenas admin).

## Licença

Este projeto está licenciado sob a Licença MIT.