from app.dao.product_dao import ProductDAO
from app.models.product import Product

class ProductService:
    def get_products(self):
        return ProductDAO.get_all()

    def get_product(self, product_id):
        return ProductDAO.get_by_id(product_id)

    def create_product(self, data):
        product = Product(**data)
        return ProductDAO.create(product)

    def update_product(self, product_id, data):
        product = ProductDAO.get_by_id(product_id)
        for key, value in data.items():
            setattr(product, key, value)
        ProductDAO.update()
        return product

    def delete_product(self, product_id):
        product = ProductDAO.get_by_id(product_id)
        ProductDAO.delete(product)
