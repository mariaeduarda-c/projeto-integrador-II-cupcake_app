import pytest
import json
# REMOVA: from app import app, db ❌
# Importe apenas o db do arquivo isolado
from database import db 
from models.product_model import Product

# ====================================================================
# FIXTURES (Usam a 'flask_app' que deve vir do conftest.py)
# ====================================================================

@pytest.fixture(scope='module')
def product_setup_client(flask_app):
    """
    Configura o banco de dados de teste (adiciona produtos) e 
    retorna o test_client.
    """
    with flask_app.app_context():
        # Limpa e cria tabelas
        db.drop_all() 
        db.create_all()
        
        # Adiciona produtos de teste
        product1 = Product(name='Test Cupcake 1', description='Desc 1', price=10.00, image_url='url1')
        product2 = Product(name='Test Cupcake 2', description='Desc 2', price=12.50, image_url='url2')
        db.session.add_all([product1, product2])
        db.session.commit()
        
    # Retorna o cliente de teste do aplicativo configurado
    yield flask_app.test_client()
    
    # Limpeza final
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

# ====================================================================
# TESTES DE ROTA (INTEGRAÇÃO)
# ====================================================================

# Troque 'test_client' pelo novo nome do fixture: product_setup_client
def test_get_all_products(product_setup_client):
    response = product_setup_client.get('/api/products')
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert len(data) == 2
    assert data[0]['name'] == 'Test Cupcake 1'
    assert data[1]['price'] == 12.50

def test_get_single_product_success(product_setup_client):
    # Assumindo que o ID 1 existe após o setup
    response = product_setup_client.get('/api/products/1') 
    assert response.status_code == 200
    data = json.loads(response.data)['data']
    assert data['name'] == 'Test Cupcake 1'
    assert data['description'] == 'Desc 1'

def test_get_single_product_not_found(product_setup_client):
    # ID que não existe
    response = product_setup_client.get('/api/products/999') 
    assert response.status_code == 404
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'Item não encontrado'