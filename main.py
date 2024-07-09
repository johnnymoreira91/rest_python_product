from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import models.productModel
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schema.productSchema import ProductSchemaInput, ProductSchemaOutput, ProductSchemaUpdate

app = FastAPI()
models.productModel.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/v1/product", response_model=List[ProductSchemaOutput])
async def list_products(db: Session = Depends(get_db)):
    products = db.query(models.productModel.Product).all()
    return products


@app.get("/v1/product/{id}", response_model=ProductSchemaOutput)
async def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(models.productModel.Product).filter(
        models.productModel.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/v1/product", response_model=ProductSchemaOutput)
async def create_product(product: ProductSchemaInput, db: Session = Depends(get_db)):
    db_product = models.productModel.Product(
        name=product.name,
        description=product.description,
        active=product.active,
        price=product.price,
        quantity=product.quantity
    )
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Product with this name already exists")
    return db_product


@app.patch("/v1/product/{id}", response_model=ProductSchemaOutput)
async def update_product(id: int, product_update: ProductSchemaUpdate, db: Session = Depends(get_db)):
    product = db.query(models.productModel.Product).filter(
        models.productModel.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Product with this name already exists")

    return product


@app.delete("/v1/product/{id}", response_model=ProductSchemaOutput)
async def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.productModel.Product).filter(
        models.productModel.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return product
