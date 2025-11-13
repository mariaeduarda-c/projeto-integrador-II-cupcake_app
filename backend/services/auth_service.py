import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db # Importa a instância do db do app principal
from models.user_model import User # Importa o modelo User diretamente

class AuthService:
    def __init__(self, db_instance, user_model):
        self.db = db_instance
        self.User = user_model

    def register_user(self, username, email, password):
        if self.User.query.filter_by(email=email).first():
            return None, "Email já registrado."

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = self.User(
            public_id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=hashed_password,
            role='user' # Novos usuários são padrão 'user'
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user, "Usuário registrado com sucesso!"

    def authenticate_user(self, email, password):
        user = self.User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None