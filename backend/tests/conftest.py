# backend/tests/conftest.py
import pytest
from app import create_app
from database import db  # Importe o db do arquivo isolado

@pytest.fixture(scope='session')
def flask_app():
    # Cria a instância do aplicativo
    app = create_app({
        'TESTING': True,
        # Use um banco de dados em memória para testes
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:' 
    })
    
    # Contexto para a aplicação (necessário para rodar o db)
    with app.app_context():
        # 🚨 MELHORIA: Importar Modelos para garantir que o SQLAlchemy os conheça!
        # Isso garante que db.create_all() crie as tabelas.
        from models.user_model import User
        from models.product_model import Product
        from models.order_model import Order 
        
        # 1. Cria todas as tabelas no banco de dados de teste
        db.create_all()
        
        # 2. Yield (Retorna) o aplicativo para que os testes possam rodar
        yield app
        
        # 3. Limpa o banco de dados após o fim da sessão de testes
        db.session.remove() # Boa prática para limpar a sessão
        db.drop_all()

@pytest.fixture(scope='function')
def client(flask_app):
    """Cria um cliente de teste para fazer requisições (injetado nos testes)."""
    return flask_app.test_client()

@pytest.fixture(scope='function')
def runner(flask_app):
    """Cria um executor de comandos de linha de comando."""
    return flask_app.test_cli_runner()