# backend/app.py (CÓDIGO REFATORADO)

from flask import Flask, request, jsonify
from database import db  
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
import uuid
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_mailman import Mail
  


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'minha_chave_secreta_muito_segura')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcake.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com') 
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT', 587)
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'marketingduda45@gmail.com') 
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'Duda10122003')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'seu_email_aqui@gmail.com')

    # Configure os dados no servidor 
    mail = Mail(app)
    # Inicializa o DB com o App
    db.init_app(app)

    # IMPORTAÇÃO DOS MÓDULOS MVC (APÓS db.init_app)

    from models.user_model import User
    from models.product_model import Product
    from models.order_model import Order
    from views.api_view import APIView
    from controllers.auth_controller import AuthController
    from controllers.product_controller import ProductController
    from controllers.admin_controller import AdminController
    from services.auth_service import AuthService
    
    #  Inicializa as classes de serviço, modelo e controller
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    auth_service = AuthService(db, User)
    auth_controller = AuthController(auth_service, APIView, mail)
    product_controller = ProductController(db, Product, APIView)
    admin_controller = AdminController(db, User, Product, APIView, UPLOAD_FOLDER)

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
        return jsonify({'message': 'Bem-vindo à API Cupcake Delícias! Servidor Flask Rodando.'})
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200
    
    @app.route('/api/login', methods=['POST'])
    def login_user():
        return auth_controller.login(app.config['SECRET_KEY'])
    @app.route('/api/forgot-password', methods=['POST'])

    def forgot_password_api():
        return auth_controller.forgot_password()
        
    @app.route('/api/reset-password', methods=['POST'])
    def reset_password_api():
        return auth_controller.reset_password()
    
    @app.route('/api/products', methods=['GET'])
    def get_all_products():
        return product_controller.get_products()

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_single_product(product_id):
        return product_controller.get_product_by_id(product_id)
    
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
    
        from models.user_model import User
        from models.product_model import Product
        
        db.create_all()
        if not User.query.filter_by(email='admin@cupcake.com').first():
            admin_user = User(
                public_id=str(uuid.uuid4()), 
                username='Administrador',
                email='admin@cupcake.com',
               
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário administrador 'admin@cupcake.com' criado com senha 'admin123'.")

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