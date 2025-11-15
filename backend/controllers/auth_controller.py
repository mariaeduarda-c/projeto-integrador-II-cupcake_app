from flask import request, jsonify, url_for
import jwt
import datetime
import secrets
from datetime import datetime, timedelta, UTC 
from flask_mailman import EmailMessage
from werkzeug.security import generate_password_hash

class AuthController:
    def __init__(self, auth_service, api_view, mail):
        self.auth_service = auth_service
        self.api_view = api_view
        self.mail = mail 

    def register(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return self.api_view.render_error('Faltam dados para o registro.', 400)

        user, message = self.auth_service.register_user(username, email, password)
        if user:
            return self.api_view.render_success(message=message, status_code=201)
        return self.api_view.render_error(message, 409) # 409 Conflict se o email já existe

    def login(self, secret_key):
        auth = request.get_json()
        email = auth.get('email')
        password = auth.get('password')

        if not email or not password:
            return self.api_view.render_error('Faltam credenciais.', 401)

        user = self.auth_service.authenticate_user(email, password)
        if not user:
            return self.api_view.render_error('Credenciais inválidas.', 401)

        # Gerar token JWT
        token = jwt.encode({
            'public_id': user.public_id,
            'role': user.role, # Inclui a função do usuário no token
            'exp': datetime.now(UTC) + timedelta(minutes=60)
        }, secret_key, algorithm="HS256")

        return self.api_view.render_success({
            'token': token,
            'role': user.role,
            'message': 'Login realizado com sucesso!'
        })
    
    def forgot_password(self):
        data = request.get_json()
        email = data.get('email')

        if not email:
            return self.api_view.render_error('E-mail é obrigatório.', 400)

        # Usamos o service para buscar o usuário (assumindo que ele tem um método para isso)
        user = self.auth_service.get_user_by_email(email)

        if user:
            # 1. Geração do Token e Expiração (1 hora)
            
            token = secrets.token_urlsafe(32)
            expiration = datetime.now(UTC) + timedelta(hours=1)
            
            # 2. Salvar no Banco de Dados

            user.reset_token = token
            user.reset_expires_at = expiration
            self.auth_service.db.session.commit()

            # 3. Enviar E-mail
    
            URL_FRONTEND = "https://projeto-integrador-ii-cupcake-app-1.onrender.com" 
            reset_url = f'{URL_FRONTEND}/reset_password.html?token={token}'

            msg = EmailMessage(
                subject='🧁 Redefinição de Senha - Cupcake Delícias',
                body=f"""
Olá,
Você solicitou a redefinição de sua senha.
Clique no link abaixo para criar uma nova senha:
{reset_url}

Este link é válido por 1 hora. Se você não solicitou esta alteração, ignore este e-mail.
""",
                to=[user.email]
            )
            self.mail.send(msg)
        
        # Sempre retornar sucesso para evitar enumeração de usuários
        return self.api_view.render_success(message='Se o e-mail estiver cadastrado, um link de redefinição foi enviado.', status_code=200)

    def reset_password(self):
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')

        if not token or not new_password:
            return self.api_view.render_error('Token e nova senha são obrigatórios.', 400)

        # Busca o usuário pelo token
        # Nota: Assumindo que você pode acessar o modelo User através de self.auth_service.User
        user = self.auth_service.db.session.query(self.auth_service.User).filter_by(reset_token=token).first()

        # 1. Validação do Token e Expiração
        if not user or user.reset_expires_at is None or user.reset_expires_at < datetime.now(UTC):
            return self.api_view.render_error('Link de redefinição inválido ou expirado.', 400)

        try:
            # 2. Atualizar Senha (Usando o mesmo método hash do register)
            user.password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
            
            # 3. Invalidar Token (Segurança: impede reutilização do link)
            user.reset_token = None
            user.reset_expires_at = None
            
            self.auth_service.db.session.commit()
            
            return self.api_view.render_success(message='Senha redefinida com sucesso. Faça login.', status_code=200)

        except Exception as e:
            self.auth_service.db.session.rollback()
            print(f"Erro ao redefinir senha: {e}")
            return self.api_view.render_error(f'Erro interno ao salvar a nova senha.', 500)