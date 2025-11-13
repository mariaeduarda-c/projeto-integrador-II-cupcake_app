import pytest
import json
import uuid
from werkzeug.security import generate_password_hash
from database import db  # Importa a instância DB isolada

# A importação dos Modelos/Serviços é feita aqui, pois não causam ciclo
# de importação com o app refatorado, mas devem ser usados dentro de um
# contexto de app (app_context) ao interagir com o DB.
from models.user_model import User
from services.auth_service import AuthService
from views.api_view import APIView

# ====================================================================
# FIXTURES (Usam a 'flask_app' que vem do conftest.py)
# ====================================================================

@pytest.fixture(scope='module')
def auth_setup_client(flask_app):
    """
    Configura o banco de dados de teste (cria usuários de exemplo) e 
    retorna o test_client.
    """
    with flask_app.app_context():
        # Limpa e cria tabelas
        db.drop_all() 
        db.create_all()
        
        # Adiciona usuários de teste
        test_user = User(
            public_id=str(uuid.uuid4()),
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123', method='pbkdf2:sha256'),
            role='user'
        )
        db.session.add(test_user)

        test_admin = User(
            public_id=str(uuid.uuid4()),
            username='adminuser',
            email='admin@example.com',
            password_hash=generate_password_hash('adminpassword', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(test_admin)
        db.session.commit()
        
    # Retorna o cliente de teste do aplicativo configurado
    yield flask_app.test_client()
    
    # Limpeza final (drop_all)
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def auth_service_fixture(flask_app):
    """
    Inicializa AuthService dentro do contexto do aplicativo de teste.
    """
    with flask_app.app_context():
        return AuthService(db, User)

@pytest.fixture(scope='module')
def admin_token(auth_setup_client): 
    """Obtém um token JWT válido para o usuário administrador."""
    response = auth_setup_client.post('/api/login', json={
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    return json.loads(response.data)['data']['token']

# ====================================================================
# TESTES DE ROTA (INTEGRAÇÃO)
# ====================================================================

def test_register_new_user(auth_setup_client):
    """Testa o registro de um novo usuário via rota API."""
    response = auth_setup_client.post('/api/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpassword'
    })
    assert response.status_code == 201
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'Usuário registrado com sucesso!'

def test_register_existing_user(auth_setup_client):
    """Testa a falha ao registrar um usuário com email duplicado."""
    response = auth_setup_client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 409
    assert 'message' in json.loads(response.data)
    assert 'Email já registrado.' in json.loads(response.data)['message']

def test_login_successful(auth_setup_client):
    """Testa o login com credenciais válidas."""
    response = auth_setup_client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert 'token' in data
    assert data['role'] == 'user'

def test_login_invalid_credentials(auth_setup_client):
    """Testa o login com senha incorreta."""
    response = auth_setup_client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'message' in json.loads(response.data)
    assert 'Credenciais inválidas.' in json.loads(response.data)['message']

# ====================================================================
# TESTES DE SERVIÇO (UNITÁRIOS)
# ====================================================================

def test_auth_service_register(auth_service_fixture):
    """Testa a lógica de registro de usuário no AuthService."""
    user, message = auth_service_fixture.register_user("serviceuser", "service@example.com", "servicepass")
    assert user is not None
    assert message == "Usuário registrado com sucesso!"
    assert user.username == "serviceuser"
    assert user.email == "service@example.com"

def test_auth_service_authenticate(auth_service_fixture):
    """Testa a autenticação de usuário no AuthService."""
    user = auth_service_fixture.authenticate_user("test@example.com", "password123")
    assert user is not None
    assert user.username == "testuser"

    invalid_user = auth_service_fixture.authenticate_user("test@example.com", "wrongpass")
    assert invalid_user is None

def test_auth_service_register_duplicate_email(auth_service_fixture):
    """Testa a falha de registro por email duplicado no AuthService."""
    user, message = auth_service_fixture.register_user("duplicate", "test@example.com", "pass")
    assert user is None
    assert message == "Email já registrado."