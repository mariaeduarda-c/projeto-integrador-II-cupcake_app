from flask import request, jsonify
import jwt
import datetime
from datetime import datetime, timedelta, UTC # <--- NOVA IMPORTAÇÃO

class AuthController:
    def __init__(self, auth_service, api_view):
        self.auth_service = auth_service
        self.api_view = api_view

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