from flask import request
from database import db 
from models.user_model import User
from models.product_model import Product
import os 
from werkzeug.utils import secure_filename 


class AdminController:
    def __init__(self, db_instance, user_model, product_model, api_view, upload_folder): 
        self.db = db_instance
        self.User = user_model
        self.Product = product_model
        self.api_view = api_view
        self.UPLOAD_FOLDER = upload_folder

    def _save_uploaded_image(self, image_file):
        if image_file:
            # Garante um nome seguro para o arquivo
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(self.UPLOAD_FOLDER, filename)
            
            # Salva o arquivo no disco
            image_file.save(filepath)
            
            # Retorna o caminho web que será salvo no banco de dados (relativo à pasta static)
            # Use 'images/' se a sua pasta static for servida como raiz no navegador
            return f'images/{filename}' 
        return None 
        
    # --- Gerenciamento de Produtos ---
    def create_product(self):
        data = request.form
        image_file = request.files.get('image_file')

        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        
        # 1. Salva o arquivo e obtém a URL
        image_url = self._save_uploaded_image(image_file) 
        
        # A URL agora é obrigatória se estamos criando
        if not all([name, description, price, image_url]):
            return self.api_view.render_error('Faltam dados ou a imagem não foi enviada/salva.', 400)

        try:
            new_product = self.Product(name=name, description=description, price=price, image_url=image_url)
            self.db.session.add(new_product)
            self.db.session.commit()
            return self.api_view.render_success(new_product.to_dict(), 'Produto criado com sucesso!', 201)
        except Exception as e:
            self.db.session.rollback()
            return self.api_view.render_error(f'Erro ao criar produto: {str(e)}', 500)


    def update_product(self, product_id):
        product = self.db.session.get(self.Product, product_id)

        if not product:
            return self.api_view.render_error('Produto não encontrado.', 404)

        if request.is_json:
            data = request.get_json()
            image_file = None # Não há upload de arquivo via JSON
        else:
            data = request.form
            image_file = request.files.get('image_file')

        # Converte o preço para float, garantindo compatibilidade com JSON e Form-data
        price_str = data.get('price')
        if price_str is not None:
            try:
                price = float(price_str)
            except ValueError:
                return self.api_view.render_error('Preço inválido.', 400)
        else:
            price = product.price # Mantém o preço original se não for enviado

        # 1. Tenta fazer o upload do novo arquivo (se existir)
        new_image_url = self._save_uploaded_image(image_file)

        try:
            # Garante que os valores vêm do dicionário 'data'
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = price # Usa o preço já convertido

            # 2. Atualiza a URL da imagem
            if new_image_url:
                product.image_url = new_image_url
            # Se for JSON e enviar 'image_url' (string), atualiza:
            elif 'image_url' in data:
                product.image_url = data['image_url'] 

            self.db.session.commit() # CORRIGE FALHA 2
            return self.api_view.render_success(product.to_dict(), 'Produto atualizado com sucesso!')
        except Exception as e:
            self.db.session.rollback()
            return self.api_view.render_error(f'Erro ao atualizar produto: {str(e)}', 500)

    def delete_product(self, product_id):
        # CORREÇÃO 4: Usando db.session.get()
        product = self.db.session.get(self.Product, product_id)
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
        # CORREÇÃO 4: Usando db.session.get()
        user = self.db.session.get(self.User, user_id)
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