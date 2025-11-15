# 🧁 Cupcake App - Projeto Integrador II

Este repositório contém todos os artefatos do projeto **"Cupcake App"**, um aplicativo de e-commerce completo projetado para uma loja virtual de cupcakes gourmet, desenvolvido como parte de um projeto integrador.

## 🚀 Links da Aplicação (Deploy)

Seu projeto está hospedado em arquitetura distribuída (Backend e Frontend separados):

| Componente | URL de Exemplo | Status |
| :--- | :--- | :--- |
| **Backend API (Render)** | `https://projeto-integrador-ii-cupcake-app-1.onrender.com` | **LIVE** |
| **Frontend (Vercel)** | `https://SEU-FRONTEND.vercel.app` | **ONLINE** |
| **Endpoint de Exemplo** | `https://projeto-integrador-ii-cupcake-app-1.onrender.com/api/products` | ✅ |

**Credenciais Admin (para teste):**
| Campo | Valor |
| :--- | :--- |
| E-mail | `admin@cupcake.com` |
| Senha | `admin123` |

---

## Tabela de Conteúdos

* [Sobre o Projeto](#sobre-o-projeto)
* [Principais Funcionalidades](#principais-funcionalidades)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Estrutura do Repositório](#estrutura-do-repositório)
* [Como Executar Localmente](#como-executar-localmente)
* [Endpoints da API RESTful](#endpoints-da-api-restful)
* [Autor](#autor)

---

## Sobre o Projeto

O **Cupcake App** é uma aplicação web completa que simula um e-commerce funcional. Ele permite aos usuários navegar por um catálogo, gerenciar um carrinho de compras e utilizar funções de autenticação.

O backend foi estruturado utilizando o microframework **Flask** e o padrão **Model-View-Controller (MVC)** para garantir a separação de responsabilidades. O sistema de autenticação utiliza **JSON Web Tokens (JWT)** para segurança das rotas administrativas.

## Principais Funcionalidades

| Área | Funcionalidades |
| :--- | :--- |
| **Cliente** | Navegação por catálogo, visualização de detalhes, adição ao carrinho, **Login**, **Cadastro** e **Recuperação de Senha**. |
| **Administrador** | Acesso ao Painel de Administração (`/admin.html`) para **Gerenciar Produtos** (CRUD) e **Gerenciar Usuários** (visualização e alteração de função/role). |
| **Geral** | Interface **Responsiva** e integração total via API RESTful. |

---

## Tecnologias Utilizadas

| Componente | Tecnologia | Detalhe |
| :--- | :--- | :--- |
| **Back-end** | **Python 3** | Linguagem principal de desenvolvimento. |
| **Framework** | **Flask** | Microframework para a criação da API RESTful. |
| **Banco de Dados** | **SQLite** | Banco de dados local para persistência (atenção à volatilidade no plano Free da Render). |
| **Autenticação** | **JWT** | Tokens JWT (JSON Web Tokens) para controle de acesso. |
| **Email** | **Flask-Mailman** | Utilizado para a funcionalidade de recuperação de senha. |
| **Front-end** | **HTML5, CSS3, JavaScript** | Desenvolvimento de interface de usuário (Vanilla JS) e lógica de requisições. |
| **Hospedagem API** | **Render** | Serviço Web utilizando Gunicorn. |
| **Hospedagem Frontend** | **Vercel** | Hospedagem estática e CDN global. |

---

## Estrutura do Repositório

O projeto é dividido em duas subpastas principais para facilitar o deploy separado (monorepo):

. ├── backend/ # Código do Servidor Python/Flask │ ├── controllers/ # Lógica da API (ex: AdminController) │ ├── models/ # Classes de dados (User, Product) │ ├── services/ # Lógica reutilizável (AuthService) │ ├── app.py # Ponto de entrada da aplicação Flask │ ├── database.py # Configuração do Flask-SQLAlchemy │ └── requirements.txt # Dependências do Python (inclui gunicorn e flask-mailman) └── frontend/ # Código da Aplicação Web (Cliente) ├── css/ # Arquivos de estilização ├── js/ # Lógica de interação e requisições AJAX ├── index.html # Página principal └── products.html # Catálogo de produtos


---

## Como Executar Localmente

Para rodar o projeto na sua máquina (Backend e Frontend), siga as instruções detalhadas:

### Pré-requisitos

* **Python 3.x**
* **pip** (gerenciador de pacotes Python)

### 1. Instalação e Setup do Backend

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/mariaeduarda-c/projeto-integrador-II-cupcake_app.git](https://github.com/mariaeduarda-c/projeto-integrador-II-cupcake_app.git)
    cd projeto-integrador-II-cupcake_app/backend
    ```
2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Execute a Aplicação:**
    ```bash
    python app.py
    ```
    ✅ O servidor estará rodando em `http://127.0.0.1:5000`.

### 2. Abrindo o Frontend

1.  Navegue até a pasta `frontend/`.
2.  Abra o arquivo **`index.html`** diretamente no seu navegador. O JavaScript fará requisições para a API rodando localmente.

---

## Endpoints da API RESTful

A API segue o padrão RESTful, com rotas abertas ao público e rotas protegidas por token JWT (`/api/admin/...`).

| Rota | Método | Descrição | Requer Token? |
| :--- | :--- | :--- | :--- |
| `/api/register` | `POST` | Cria uma nova conta de usuário. | Não |
| `/api/login` | `POST` | Gera um token de autenticação (JWT). | Não |
| `/api/forgot-password` | `POST` | Envia e-mail para recuperação de senha. | Não |
| `/api/products` | `GET` | Lista todos os produtos disponíveis. | Não |
| `/api/admin/products` | `POST` | Cria um novo produto (CRUD). | Sim (Admin) |
| `/api/admin/users/<id>/role` | `PUT` | Altera a função (`user`/`admin`) de um usuário. | Sim (Admin) |

---

## Autor

- **Nome:** Renan Rodrigo Fernandes de Sousa
- **RGM:** 30064597
- **Curso:** Engenharia de Software
- **Instituição:** Universidade Positivo