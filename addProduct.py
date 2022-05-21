#!/usr/bin/python
from models import Base, Product, Barcode
from sqlalchemy import func
from database import Session, engine

Base.metadata.create_all(bind=engine)

while True:
    with Session() as session:
        name = input("Product name: ")
        price = input("Price in cents: ")
        code = input("Barcode: ")
        
        product = Product(name=name, price=price, amount=0)
        barcode = Barcode(barcode=code, product_id=product.id)
        session.add_all([product, barcode])
        session.commit()