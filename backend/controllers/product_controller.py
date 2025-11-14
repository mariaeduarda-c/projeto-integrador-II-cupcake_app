from flask import request, url_for, current_app 
from database import db
from models.product_model import Product
from werkzeug.exceptions import InternalServerError # Para um tratamento de erro mais limpo

class ProductController:
    def __init__(self, db_instance, product_model, api_view):
        self.db = db_instance
        self.Product = product_model
        self.api_view = api_view

    def get_products(self):
        """
        Busca todos os produtos e gera a URL absoluta da imagem usando url_for.
        """
        try:
            products = self.Product.query.all()
            products_list_with_urls = []

            # 💡 Garante que a URL_FOR funcione dentro do contexto do app
            with current_app.app_context():
                for product in products:
                    product_dict = product.to_dict()
                    
                    db_image_path = product_dict['image_url']

                    try:
                        product_dict['image_url'] = url_for('static', filename=db_image_path, _external=True)
                    except Exception as e:
                        print(f"ATENÇÃO: Não foi possível gerar URL para o produto ID {product_dict['id']}. Erro: {e}")
                        product_dict['image_url'] = '/static/images/placeholder.jpg' 

                    products_list_with_urls.append(product_dict)
            
            # Retorna a resposta no formato esperado pelo frontend (data: [...])
            return self.api_view.render_success(
                data=products_list_with_urls, 
                message="Lista de produtos carregada."
            )
            
        except Exception as e:
            # Tratamento de erro geral para garantir que a API não caia com 500
            print(f"Erro crítico ao carregar produtos: {e}")
            return self.api_view.render_error("Erro interno ao carregar produtos.", 500)

    def get_product_by_id(self, product_id):
        product = self.Product.query.get(product_id)
        
        if not product:
             return self.api_view.render_error("Produto não encontrado.", 404)

        product_dict = product.to_dict()
        
        with current_app.app_context():
            try:
                product_dict['image_url'] = url_for('static', filename=product_dict['image_url'], _external=True)
            except Exception:
                product_dict['image_url'] = '/static/images/placeholder.jpg'

        return self.api_view.render_success(data=product_dict, message="Produto encontrado.")