# 🧁 Cupcake App - Projeto Integrador II

![Status](https://img.shields.io/badge/status-Projeto%20Concluído-brightgreen)
![Linguagem](https://img.shields.io/badge/Linguagem-Python%203-blue)
![Framework](https://img.shields.io/badge/Back--end-Flask-red)
![Banco de Dados](https://img.shields.io/badge/Database-SQLite-orange)
![Autenticação](https://img.shields.io/badge/Auth-JWT-yellow)
![Front-end](https://img.shields.io/badge/Front--end-HTML%2FJS%2FCSS-informational)

Este repositório reúne todos os produtos desenvolvidos para o projeto **"Cupcake App"**. Este projeto é um requisito da disciplina **Projeto Integrador Transdisciplinar em Engenharia de Software II** do curso de Engenharia de Software da Universidade Positivo.

## 🚀 Links da Aplicação (Deploy)

O projeto está hospedado em arquitetura distribuída (Backend e Frontend separados):

| Componente | URL de Exemplo | Status |
| :--- | :--- | :--- |
| **Backend API (Render)** | `https://projeto-integrador-ii-cupcake-app-1.onrender.com` | **LIVE** |
| **Frontend (Vercel)** | `https://projeto-integrador-ii-cupcake-app-w.vercel.app/` | **ONLINE** |
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

* **`/backend`**: Contém todo o código-fonte do **servidor Python/Flask** (API RESTful).
    * **`controllers/`**: Lógica da **API** (Controller layer), onde estão as rotas e o tratamento das requisições (ex: `AdminController`, `ProductController`).
    * **`models/`**: **Classes de dados** (Model layer), que representam as entidades do banco de dados (ex: `User`, `Product`).
    * **`services/`**: **Lógica de Negócio** reutilizável, separada das controllers (ex: funções de autenticação em `AuthService`).
    * **`app.py`**: O **ponto de entrada** principal da aplicação Flask.
    * **`database.py`**: Configuração e inicialização do **Flask-SQLAlchemy**.
    * **`requirements.txt`**: Lista de **dependências Python** necessárias para execução (inclui `Flask`, `gunicorn` e `flask-mailman`).
    * **`tests/`**: Testes unitários para a camada de Back-end (executados com `pytest`).

* **`/frontend`**: Contém todo o código-fonte da **Aplicação Web Cliente** (HTML, CSS e JavaScript).
    * **`css/`**: Arquivos de **estilização** (CSS).
    * **`js/`**: **Lógica de interação** e todas as **requisições AJAX** para a API Back-end.
    * **`index.html`**: A **Página Principal** da aplicação.
    * **`products.html`**: A página do **Catálogo de Produtos**.
    * *Outras páginas* (ex: `admin.html`, `login.html`, etc.).

---

## Como Executar Localmente

Para rodar o projeto na máquina (Backend e Frontend), siga as instruções detalhadas:

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

### 🧪 Testes Unitários e Qualidade

Conforme as diretrizes do projeto, foram implementados **Testes Unitários** no Back-end, utilizando o **Pytest**, como parte do processo de garantia de qualidade do código.

#### Testes Unitários (Back-end)
* **Framework de Teste:** **Pytest**.
* **Cobertura:** Os testes foram focados na validação da **lógica de negócio** e na **segurança das rotas** da API (Autenticação e CRUD de Admin).
* **Localização dos Testes:** As classes de teste estão localizadas no diretório `/backend/tests/` do repositório.

As áreas chave testadas incluem:
* **`test_auth.py`**: Testes de registro, login e geração de JWT. (3 testes)
* **`test_products_crud.py`**: Testes das operações CRUD (Create, Read, Update, Delete) de produtos. (4 testes)
* **`test_admin_users.py`**: Testes de gerenciamento de usuários por admin (visualização e alteração de `role`). (3 testes)

| Total de Testes | Status | Comando de Execução |
| :---: | :---: | :---: |
| **10** | ✅ **Todos Passam** | `pytest` (no diretório `/backend`) |

**Resultado:** Todos os 10 testes unitários passam com sucesso quando executados localmente, confirmando que as lógicas de autenticação e as regras de negócio principais para o administrador estão funcionando conforme o esperado.

#### Testes de Validação (Front-end/Integração)
Além dos testes automatizados, foi realizada a **validação manual** completa da aplicação Web (Front-end integrado com o Back-end) para garantir a usabilidade e a correta integração de ponta a ponta (e.g., carrinho de compras, checkout e painel administrativo).

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

### 📈 Status e Conclusão do Projeto (Marco Finalizado)

O projeto seguiu um ciclo de desenvolvimento estruturado, com todas as fases (Situações-Problema - SP) concluídas com sucesso e prontas para entrega final.

| Fase | Título | Entregáveis Principais |
| :--- | :--- | :--- |
| **✅ SP1** | **Planejamento e Modelagem** | O ciclo de planejamento foi **finalizado**. O **Banco de Dados (SQLite)** foi **modelado** e sua documentação estrutural foi concluída. |
| **✅ SP2** | **Desenvolvimento e Integração** | As implementações do **Back-end (Python/Flask)** e **Front-end (Web)** foram **concluídas e integradas**. O desenvolvimento inicial incluiu a implementação dos **Testes Unitários** no servidor. |
| **✅ SP3** | **Validação e Melhoria Contínua** | Esta fase focou na **qualidade e usabilidade**. Foi coletado **feedback de pares** e implementadas melhorias críticas no Front-end (ex: estados de Loading, feedback de usuário e esvaziamento do carrinho). O **Laudo de Qualidade** foi produzidos e anexados. |

**Status Final:** O projeto atingiu 100% dos requisitos de entrega, incluindo o preenchimento e finalização do documento **PIT_atividade.docx**.

## Autor

- **Nome:** Maria Eduarda Caixeta do Sacramento 
- **RGM:** 30330378
- **Curso:** Engenharia de Software
- **Instituição:** Cruzeiro do Sul Virtual / Polo: UDF - Centro Universitário  
 