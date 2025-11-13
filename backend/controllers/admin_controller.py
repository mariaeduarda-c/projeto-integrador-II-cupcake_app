from flask import request
from database import db # Importa a instância do db do app principal
from models.user_model import User
from models.product_model import Product

class AdminController:
    def __init__(self, db_instance, user_model, product_model, api_view):
        self.db = db_instance
        self.User = user_model
        self.Product = product_model
        self.api_view = api_view

    # --- Gerenciamento de Produtos ---
    def create_product(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        image_url = data.get('image_url')

        if not all([name, description, price]):
            return self.api_view.render_error('Faltam dados para criar o produto.', 400)

        try:
            new_product = self.Product(name=name, description=description, price=price, image_url=image_url)
            self.db.session.add(new_product)
            self.db.session.commit()
            return self.api_view.render_success(new_product.to_dict(), 'Produto criado com sucesso!', 201)
        except Exception as e:
            self.db.session.rollback()
            return self.api_view.render_error(f'Erro ao criar produto: {str(e)}', 500)

    def update_product(self, product_id):
        product = self.Product.query.get(product_id)
        if not product:
            return self.api_view.render_error('Produto não encontrado.', 404)

        data = request.get_json()
        try:
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.image_url = data.get('image_url', product.image_url)
            self.db.session.commit()
            return self.api_view.render_success(product.to_dict(), 'Produto atualizado com sucesso!')
        except Exception as e:
            self.db.session.rollback()
            return self.api_view.render_error(f'Erro ao atualizar produto: {str(e)}', 500)

    def delete_product(self, product_id):
        product = self.Product.query.get(product_id)
        if not product:
            return self.api_view.render_error('Produto não encontrado.', 404)

        try:
            self.db.session.delete(product)
            self.db.session.commit()
            return self.api_view.render_success(message='Produto excluído com sucesso!', status_code=204) # 204 No Content
        except Exception as e:
            self.db.session.rollback()
            return self.api_view.render_error(f'Erro ao excluir produto: {str(e)}', 500)

    # --- Gerenciamento de Usuários ---
    def get_users(self):
        users = self.User.query.all()
        return self.api_view.render_items(users, "Lista de usuários.")

    def update_user_role(self, user_id):
        user = self.User.query.get(user_id)
        if not user:
            return self.api_view.render_error('Usuário não encontrado.', 404)

        data = request.get_json()
        new_role = data.get('role')

        if not new_role or new_role not in ['user', 'admin']:
            return self.api_view.render_error('Função inválida. Use "user" ou "admin".', 400)

        try:
            user.role = new_role
            self.db.session.commit()
            return self.api_view.render_success(user.to_dict(), f'Função do usuário {user.username} atualizada para {new_role} com sucesso!')
        except Exception as e:
            self.db.session.rollback()
            return self.api_view.render_error(f'Erro ao atualizar função do usuário: {str(e)}', 500)