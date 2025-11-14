import pytest
import json
import uuid # Necessário para gerar public_id
import datetime
from datetime import UTC
import jwt
from werkzeug.security import generate_password_hash
# Importe db do arquivo isolado. O 'app' será injetado pelo pytest.
from database import db 
from models.user_model import User
from models.product_model import Product

# ====================================================================
# FIXTURES (Usam a 'flask_app' que vem do conftest.py)
# Renomeei 'test_client' para 'admin_setup_client' para evitar conflito com 'client' do conftest
# ====================================================================

@pytest.fixture(scope='module')
def admin_setup_client(flask_app):
    """
    Configura o banco de dados de teste (cria usuários/produtos de exemplo) 
    e retorna o test_client.
    """
    with flask_app.app_context():
        # Limpa o DB antes de criar novos dados
        db.drop_all()
        db.create_all()

        # Adiciona um usuário admin
        admin_user = User(
            public_id=str(uuid.uuid4()), # Use uuid.uuid4()
            username='adminuser',
            email='admin@test.com',
            password_hash=generate_password_hash('adminpass', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin_user)

        # Adiciona um usuário normal
        regular_user = User(
            public_id=str(uuid.uuid4()), # Use uuid.uuid4()
            username='regularuser',
            email='user@test.com',
            password_hash=generate_password_hash('userpass', method='pbkdf2:sha256'),
            role='user'
        )
        db.session.add(regular_user)

        # Adiciona um produto de teste inicial
        initial_product = Product(name='Initial Product', description='Initial Desc', price=5.00, image_url='initial.jpg')
        db.session.add(initial_product)
        db.session.commit()
        
    # Retorna o cliente de teste do aplicativo configurado
    yield flask_app.test_client()
    
    # Limpeza final (drop_all)
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def admin_token(admin_setup_client, flask_app): # Recebe flask_app para acessar config
    """Gera um token JWT válido para o usuário administrador."""
    with flask_app.app_context():
        # Gerar um token diretamente para o admin_user
        admin_user = User.query.filter_by(email='admin@test.com').first()
        token = jwt.encode({
            'public_id': admin_user.public_id,
            'role': admin_user.role,
            'exp': datetime.datetime.now(UTC) + datetime.timedelta(minutes=60)
    }, flask_app.config['SECRET_KEY'], algorithm="HS256")
    return token

@pytest.fixture(scope='module')
def user_token(admin_setup_client, flask_app): # Recebe flask_app para acessar config
    """Gera um token JWT válido para o usuário normal."""
    with flask_app.app_context():
        # Gerar um token diretamente para o regular_user
        regular_user = User.query.filter_by(email='user@test.com').first()
        token = jwt.encode({
            'public_id': regular_user.public_id,
            'role': regular_user.role,
            'exp': datetime.datetime.now(UTC) + datetime.timedelta(minutes=60)
    }, flask_app.config['SECRET_KEY'], algorithm="HS256")
    return token

# ====================================================================
# TESTES DE PRODUTOS ADMIN
# ====================================================================

# Recebe admin_setup_client (o cliente de teste configurado)
def test_admin_create_product(admin_setup_client, admin_token):
    from io import BytesIO 

    # 1. Dados de texto
    new_product_data = {
        'name': 'New Admin Cupcake',
        'description': 'Description of new cupcake',
        'price': '9.99',  # Envie como string se o controller for ler de request.form
    }

    image_content = b'image data placeholder' 
    image_file = (BytesIO(image_content), 'test_cupcake.jpg')

    response = admin_setup_client.post(
        '/api/admin/products', 
        data={**new_product_data, 'image_file': image_file}, # Combina dados de texto e arquivo
        headers={'Authorization': f'Bearer {admin_token}'},
        content_type='multipart/form-data' # Especifica o tipo de conteúdo
    )

def test_admin_create_product_unauthorized(admin_setup_client, user_token):
    new_product_data = {
        'name': 'Unauthorized Cupcake',
        'description': 'Description',
        'price': 1.00,
        'image_url': 'unauth.jpg'
    }
    response = admin_setup_client.post('/api/admin/products', json=new_product_data, headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 403 

def test_admin_create_product_no_token(admin_setup_client):
    new_product_data = {'name': 'No Token Cupcake', 'description': 'Desc', 'price': 1.00, 'image_url': 'notoken.jpg'}
    response = admin_setup_client.post('/api/admin/products', json=new_product_data)
    assert response.status_code == 401 

def test_admin_update_product(admin_setup_client, admin_token, flask_app):
    # Deve usar o contexto do app para fazer consultas ao DB
    with flask_app.app_context():
        product_to_update = Product.query.filter_by(name='Initial Product').first()
        product_id = product_to_update.id

    updated_data = {
        'name': 'Updated Product Name',
        'price': 15.00
    }
    response = admin_setup_client.put(f'/api/admin/products/{product_id}', json=updated_data, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert data['name'] == 'Updated Product Name'
    assert data['price'] == 15.00

def test_admin_update_nonexistent_product(admin_setup_client, admin_token):
    response = admin_setup_client.put('/api/admin/products/999', json={'name': 'Nonexistent'}, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 404
    assert 'Produto não encontrado.' in json.loads(response.data)['message']

def test_admin_delete_product(admin_setup_client, admin_token, flask_app):
    # Cria e deleta o produto DENTRO do contexto do app
    with flask_app.app_context():
        # Cria um produto temporário para deletar
        temp_product = Product(name='Temp Product', description='Temp Desc', price=1.0, image_url='temp.jpg')
        db.session.add(temp_product)
        db.session.commit()
        temp_product_id = temp_product.id
    
    response = admin_setup_client.delete(f'/api/admin/products/{temp_product_id}', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 204 # No Content for successful deletion
    
    # Verifica se o produto foi realmente deletado
    with flask_app.app_context():
        deleted_product = Product.query.get(temp_product_id)
        assert deleted_product is None

def test_admin_delete_nonexistent_product(admin_setup_client, admin_token):
    response = admin_setup_client.delete('/api/admin/products/999', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 404
    assert 'Produto não encontrado.' in json.loads(response.data)['message']

# ====================================================================
# TESTES DE USUÁRIOS ADMIN
# ====================================================================

def test_admin_get_all_users(admin_setup_client, admin_token):
    response = admin_setup_client.get('/api/admin/users', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert len(data) >= 2 # admin_user e regular_user
    assert any(u['email'] == 'admin@test.com' for u in data)
    assert any(u['email'] == 'user@test.com' for u in data)

def test_admin_get_all_users_unauthorized(admin_setup_client, user_token):
    response = admin_setup_client.get('/api/admin/users', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 403 

def test_admin_update_user_role(admin_setup_client, admin_token, flask_app):
    with flask_app.app_context():
        # Recria um usuário temporário para evitar conflitos de sessão
        temp_user = User(
            public_id=str(uuid.uuid4()),
            username='temp_role_user',
            email='temp_role@test.com',
            password_hash=generate_password_hash('temp_pass', method='pbkdf2:sha256'),
            role='user'
        )
        db.session.add(temp_user)
        db.session.commit()
        user_id = temp_user.id

    response = admin_setup_client.put(f'/api/admin/users/{user_id}/role', json={'role': 'admin'}, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert data['email'] == 'temp_role@test.com'
    assert data['role'] == 'admin'

    # Verifica se a função foi realmente atualizada no DB
    with flask_app.app_context():
        updated_user = User.query.get(user_id)
        assert updated_user.role == 'admin'

def test_admin_update_user_role_invalid_role(admin_setup_client, admin_token, flask_app):
    with flask_app.app_context():
        user_to_update = User.query.filter_by(email='admin@test.com').first()
        user_id = user_to_update.id
    
    response = admin_setup_client.put(f'/api/admin/users/{user_id}/role', json={'role': 'superadmin'}, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 400
    assert 'Função inválida.' in json.loads(response.data)['message']

def test_admin_update_nonexistent_user_role(admin_setup_client, admin_token):
    response = admin_setup_client.put('/api/admin/users/999/role', json={'role': 'admin'}, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 404
    assert 'Usuário não encontrado.' in json.loads(response.data)['message']