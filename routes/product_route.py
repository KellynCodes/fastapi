
from fastapi import APIRouter
from data.db import engine, Base, SessionLocal
from models.models import Product
from schemas.schema import ProductSchema
class ProductController():
    router = APIRouter()
    
    def __init__(self):
        Base.metadata.create_all(bind=engine)
        self.router.post("/")(self.create_product)
        self.router.get("/{productId}")(self.get_product)
        self.router.put("/{productId}")(self.update_product)
        self.router.delete("/{productId}")(self.delete_product)
    
    def create_product(self, product: ProductSchema): 
        db = SessionLocal()
        new_product = Product(name=product.name, description=product.description, quantity=product.quantity,price=product.price)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        db.close()
        return new_product
    
    def get_product(self, product_id: int):
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()
        db.close()
        if not product:
            return {"error": "Product not found."}
        return product 
    
    def update_product(self, product_id: int, model: ProductSchema):
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            db.close()
            return {"Error": "Product not found."}
        
        product.name = model.name
        product.description = model.description
        product.price = model.price
        product.quantity = model.quantity
        
        db.commit()
        db.refresh(product)
        db.close()
        return product
    
    def delete_product(self, product_id: int):
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            db.close()
            return {"error": "Product does not exist"}
        db.delete(product)
        db.commit()
        db.close()
        return {"message": "Product deleted"}