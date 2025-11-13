from flask import request
from database import db # Importa a instância do db do app principal
from models.product_model import Product # Importa o modelo Product

class ProductController:
    def __init__(self, db_instance, product_model, api_view):
        self.db = db_instance
        self.Product = product_model
        self.api_view = api_view

    def get_products(self):
        products = self.Product.query.all()
        return self.api_view.render_items(products, "Lista de produtos.")

    def get_product_by_id(self, product_id):
        product = self.Product.query.get(product_id)
        return self.api_view.render_item(product, "Produto encontrado.")