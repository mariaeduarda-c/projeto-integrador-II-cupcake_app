# backend/setup_db.py

from app import create_app
from database import db
from models.user_model import User
from models.product_model import Product
from werkzeug.security import generate_password_hash
import uuid

app = create_app()

with app.app_context():
    # 1. Cria todas as tabelas (db.create_all())
    db.create_all()
    print("Tabelas do Banco de Dados criadas com sucesso.")

    # 2. Insere o usuário Admin se ele não existir
    if not User.query.filter_by(email='admin@cupcake.com').first():
        admin_user = User(
            public_id=str(uuid.uuid4()),
            username='Administrador',
            email='admin@cupcake.com',
            password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin_user)
        print("Usuário administrador 'admin@cupcake.com' criado.")

    # 3. Insere os Produtos de Exemplo se não existirem
    if not Product.query.first():
        products_data = [
            {'name': 'Cupcake de Chocolate', 'description': 'Delicioso cupcake de chocolate com cobertura de ganache.', 'price': 7.50, 'image_url': '../images/cupcake1.jpg'},
            # Adicione aqui o restante dos seus produtos de exemplo
        ]
        for p_data in products_data:
            new_product = Product(**p_data)
            db.session.add(new_product)
        print(f"{len(products_data)} produtos de exemplo adicionados.")
        
    db.session.commit()