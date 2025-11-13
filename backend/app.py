# backend/app.py (CÓDIGO REFATORADO)

from flask import Flask, request, jsonify
from database import db  # 👈 AGORA IMPORTAMOS DO database.py!
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
import uuid
from flask_cors import CORS
  # Adicione o uuid para gerar public_id

# IMPORTAÇÕES DE MÓDULOS MVC REMOVIDAS DAQUI
# MOVIDAS PARA DENTRO DE create_app()

def create_app(test_config=None):
    app = Flask(__name__)
    # Substitua '5500' pela porta que seu Live Server estiver usando
    CORS(app)

    # Configuração do Flask
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'minha_chave_secreta_muito_segura')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcake.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)
    
    # 1. Inicializa o DB com o App
    db.init_app(app)

    # 2. IMPORTAÇÃO DOS MÓDULOS MVC (APÓS db.init_app)
    # Isso quebra o ciclo de importação
    from models.user_model import User
    from models.product_model import Product
    from models.order_model import Order
    from views.api_view import APIView
    from controllers.auth_controller import AuthController
    from controllers.product_controller import ProductController
    from controllers.admin_controller import AdminController
    from services.auth_service import AuthService
    
    # 3. Inicializa as classes de serviço, modelo e controller
    auth_service = AuthService(db, User)
    auth_controller = AuthController(auth_service, APIView)
    product_controller = ProductController(db, Product, APIView)
    admin_controller = AdminController(db, User, Product, APIView)

    # -----------------------------------------------------------
    # Decoradores (Definidos DENTRO da função ou usando o app que foi criado)
    # -----------------------------------------------------------
    
    # Decorador para verificar token JWT
    # Usa o 'app' que acabou de ser criado
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Token é necessário!'}), 401

            try:
                # Usa app.config['SECRET_KEY'] da instância atual do app
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expirado. Faça login novamente.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token inválido!'}), 401

            return f(current_user, *args, **kwargs)
        return decorated

    # Decorador para verificar se o usuário é admin
    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Token é necessário!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.filter_by(public_id=data['public_id']).first()

                if not current_user or current_user.role != 'admin':
                    return jsonify({'message': 'Acesso negado: Apenas administradores podem realizar esta ação.'}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expirado. Faça login novamente.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token inválido!'}), 401

            return f(current_user, *args, **kwargs)
        return decorated

    # -----------------------------------------------------------
    # Rotas (Definidas DENTRO da função)
    # -----------------------------------------------------------

    # Rotas de Autenticação
    @app.route('/api/register', methods=['POST'])
    def register_user():
        return auth_controller.register()
    
    @app.route('/', methods=['GET'])
    def home():
        # Retorna uma resposta JSON simples para confirmar que o servidor está funcionando
        return jsonify({'message': 'Bem-vindo à API Cupcake Delícias! Servidor Flask Rodando.'})
    # 👆 FIM DA ADIÇÃO

    @app.route('/api/login', methods=['POST'])
    def login_user():
        # Passa a chave secreta para o controlador, se necessário
        return auth_controller.login(app.config['SECRET_KEY'])

    # Rotas de Produtos (públicas)
    @app.route('/api/products', methods=['GET'])
    def get_all_products():
        return product_controller.get_products()

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_single_product(product_id):
        return product_controller.get_product_by_id(product_id)

    # Rotas de Administração (requer token e role 'admin')
    @app.route('/api/admin/products', methods=['POST'])
    @admin_required
    def create_product(current_user): 
        return admin_controller.create_product()

    @app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
    @admin_required
    def update_product(current_user, product_id):
        return admin_controller.update_product(product_id)

    @app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
    @admin_required
    def delete_product(current_user, product_id):
        return admin_controller.delete_product(product_id)

    @app.route('/api/admin/users', methods=['GET'])
    @admin_required
    def get_all_users(current_user):
        return admin_controller.get_users()

    @app.route('/api/admin/users/<int:user_id>/role', methods=['PUT'])
    @admin_required
    def update_user_role(current_user, user_id):
        return admin_controller.update_user_role(user_id)

    return app

# -----------------------------------------------------------
# Bloco de Inicialização (Executado apenas quando o arquivo é rodado diretamente)
# -----------------------------------------------------------

if __name__ == '__main__':
    app = create_app()
    
    # 1. Inicialização do Banco de Dados e Dados Iniciais
    with app.app_context():
        # Importações locais necessárias para garantir que os Modelos sejam carregados
        from models.user_model import User
        from models.product_model import Product
        
        db.create_all()

        # Adicionar um usuário admin se não existir
        if not User.query.filter_by(email='admin@cupcake.com').first():
            admin_user = User(
                public_id=str(uuid.uuid4()), # Geração correta do public_id
                username='Administrador',
                email='admin@cupcake.com',
                # Certifique-se de que generate_password_hash está importado
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário administrador 'admin@cupcake.com' criado com senha 'admin123'.")

        # Adicionar produtos de exemplo
        if not Product.query.first():
            products_data = [
                {'name': 'Cupcake de Chocolate', 'description': 'Delicioso cupcake de chocolate com cobertura de ganache.', 'price': 7.50, 'image_url': '../images/cupcake1.jpg'},
                {'name': 'Cupcake de Baunilha', 'description': 'Clássico cupcake de baunilha com buttercream.', 'price': 6.00, 'image_url': '../images/cupcake2.jpg'},
                {'name': 'Cupcake Red Velvet', 'description': 'O famoso red velvet com cobertura de cream cheese.', 'price': 8.00, 'image_url': '../images/cupcake3.jpg'},
                {'name': 'Cupcake Limão', 'description': 'Refrescante cupcake de limão com merengue suíço.', 'price': 7.00, 'image_url': '../images/cupcake4.jpg'}
            ]
            for p_data in products_data:
                new_product = Product(**p_data)
                db.session.add(new_product)
            db.session.commit()
            print("Produtos de exemplo adicionados.")

    # 2. Executa o App
    app.run(debug=True)