# 🧁 Cupcake App - E-commerce de Cupcakes Gourmet

Este repositório contém todos os artefatos do projeto "Cupcake App", um aplicativo de e-commerce completo projetado para uma loja virtual de cupcakes gourmet. O objetivo é simular uma aplicação real de ponta a ponta, desde o catálogo de produtos até o painel administrativo.

---

## 💡 Sobre o Projeto

O **Cupcake App** é uma aplicação web completa que permite aos usuários navegar por um catálogo virtual, gerenciar um carrinho de compras e realizar a jornada de checkout.

O projeto foi estruturado para demonstrar o conhecimento em arquitetura e desenvolvimento web, utilizando o padrão **Model-View-Controller (MVC)** no backend para garantir a separação de responsabilidades e facilitar a manutenção.

### Principais Funcionalidades

| Área | Funcionalidades |
| :--- | :--- |
| **Cliente** | Navegação por catálogo de produtos, visualização de detalhes, adição/remoção de itens no carrinho, **Cadastro (Register)** e **Login** para simular o checkout. |
| **Administrador** | Acesso ao Painel de Administração (`/admin.html`) para **Gerenciar Produtos** (CRUD) e **Gerenciar Usuários** (visualização e alteração de função/role). |
| **Geral** | Interface **Responsiva** (Desktop e Mobile) e integração completa via API RESTful. |

---

## 💻 Tecnologias Utilizadas

| Componente | Tecnologia | Detalhe |
| :--- | :--- | :--- |
| **Front-end** | **HTML5, CSS3, JavaScript** | Desenvolvimento de interface do usuário, responsividade e lógica de requisições. |
| **Back-end** | **Python 3** | Linguagem principal de desenvolvimento. |
| **Framework** | **Flask** | Microframework para a criação da API RESTful. |
| **Banco de Dados** | **SQLite** | Banco de dados simples para prototipagem e persistência local. |
| **Padrão** | **MVC** | Organização da lógica do backend (Controllers, Models, Views). |
| **Autenticação** | **JWT** | Tokens JWT (JSON Web Tokens) para controle de acesso (Login e rotas de Admin). |

---

## 📂 Estrutura do Repositório

O projeto é dividido em `frontend/` (Cliente) e `backend/` (Servidor/API).

. ├── backend/ │ ├── controllers/ # Lógica da API (ex: AdminController, ProductController). │ ├── models/ # Classes de dados (ex: User, Product). │ ├── views/ # Formatação de respostas JSON (APIView). │ ├── services/ # Lógica reutilizável (ex: funções de autenticação). │ ├── tests/ # Testes unitários do backend (pytest). │ ├── app.py # Ponto de entrada da aplicação Flask. │ └── database.py # Configuração do Flask-SQLAlchemy. └── frontend/ ├── css/ # Arquivos de estilização (style.css). ├── js/ # Lógica de interação e requisições AJAX. ├── index.html # Página principal. ├── products.html # Catálogo de produtos. └── ...demais páginas.


---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* **Python 3.x**
* **pip** (gerenciador de pacotes Python)

### 1. Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/cupcake_app.git](https://github.com/seu-usuario/cupcake_app.git)
    cd cupcake_app
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências do back-end:**
    ```bash
    pip install Flask Flask-SQLAlchemy Werkzeug pytest PyJWT
    ```

### 2. Executando o Back-end (API)

1.  Navegue até a pasta `backend/`:
    ```bash
    cd backend
    ```

2.  Execute o servidor Flask:
    ```bash
    python app.py
    ```
    ✅ O servidor estará rodando em **`http://127.0.0.1:5000`**.

### 3. Abrindo o Front-end (Cliente)

1.  Abra a pasta `frontend/`.
2.  Abra o arquivo **`index.html`** diretamente no seu navegador (ex: `file:///caminho/para/frontend/index.html`).
    *O JavaScript fará requisições para a API rodando localmente.*

---

## 🧪 Testes Unitários

Para garantir a confiabilidade da lógica de negócios e das rotas de administração.

1.  Navegue até a pasta `backend/`:
    ```bash
    cd backend
    ```

2.  Execute os testes usando `pytest`:
    ```bash
    pytest
    ```
    *(Você verá a saída dos testes, confirmando que todos os endpoints de CRUD e autenticação estão funcionando.)*

---

## 🧭 Endpoints da API RESTful (Back-end)

| Rota | Método | Descrição | Requer Token? |
| :--- | :--- | :--- | :--- |
| `/api/register` | `POST` | Cria uma nova conta de usuário. | Não |
| `/api/login` | `POST` | Gera um token de autenticação (JWT). | Não |
| `/api/products` | `GET` | Lista todos os produtos disponíveis. | Não |
| `/api/products/<id>` | `GET` | Detalhes de um produto específico. | Não |
| `/api/admin/products` | `POST` | Cria um novo produto no catálogo. | Sim (Admin) |
| `/api/admin/products/<id>`| `PUT` | Atualiza um produto existente. | Sim (Admin) |
| `/api/admin/products/<id>`| `DELETE` | Remove um produto do catálogo. | Sim (Admin) |
| `/api/admin/users` | `GET` | Lista todos os usuários cadastrados. | Sim (Admin) |
| `/api/admin/users/<id>/role`| `PUT` | Altera a função (role) de um usuário (user/admin). | Sim (Admin) |

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**.

---

# Autor

- **Nome:** Maria Eduarda Caixeta do Sacramento
- **RGM:** 30330378
- **Curso:** Engenharia de Software
- **Instituição:** Cruzeiro do Sul Virtual 