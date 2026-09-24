from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlmodel import select
from src.models.product_model import Product
from src.shared.database.session_db import SessionDep, get_session
from enum import Enum


app = FastAPI()

# Clase para definir los productos permitidos
class AllowedProducts(str, Enum):
    MONITORES = "monitores"
    MOUSE = "mouse"
    TECLADO = "teclado"

# Clase para crear un nuevo producto con validaciones
class CreateProduct(BaseModel):
    name: AllowedProducts = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=10000)
    quantity: int = Field(..., ge=0)
    category: str = Field(..., )

# Validador que asegura que el nombre del producto esté en minúsculas y sin espacios antes de la validación
# Normalizador para el Enum (name)
@field_validator("name", mode="before")
@classmethod
def normalize_name(cls, value: str) -> str:
    """Sanea el texto y lo pasa a minúsculas ANTES de validar contra el Enum."""
    if isinstance(value, str): # isinstance es una función que verifica si un objeto es una instancia de una clase o de una subclase de esa clase. En este caso, se está verificando si value es una cadena de texto (str).
        return value.strip().lower()
    return value
# Validador que asegura que la categoría del producto esté en minúsculas y sin espacios antes de la validación
# Normalizador para la categoría
@field_validator("category", mode="before")
@classmethod
def normalize_category(cls, value: str) -> str:
    """Sanea el texto y lo pasa a minúsculas ANTES de guardar."""
    if isinstance(value, str): # isinstance es una función que verifica si un objeto es una instancia de una clase o de una subclase de esa clase. En este caso, se está verificando si value es una cadena de texto (str).
        return value.strip().lower()
    return value

# Crea un nuevo producto
@app.post(
        "/product",
    response_model=Product,
    status_code=status.HTTP_201_CREATED, # El código de estado HTTP 201 indica que la solicitud se ha completado con éxito y que se ha creado un nuevo recurso como resultado. En este caso, se está creando un nuevo producto en la base de datos.
    summary="Crear un nuevo producto"
    )

def create_product(product: CreateProduct, session: SessionDep):
    # 1. --- Validación de nombre duplicado ---
    existing_product = session.exec( 
        
        select(Product).where(Product.name == product.name)
    ).first()
# Session.exec() es un método que ejecuta una consulta SQL en la base de datos y devuelve un objeto Result que contiene los resultados de la consulta. En este caso, se está ejecutando una consulta para buscar un producto existente con el mismo nombre que el producto que se está intentando crear.

    if existing_product: 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El nombre '{product.name}' ya está registrado."
        )
  # Si se encuentra un producto existente con el mismo nombre, se lanza una excepción HTTPException con un código de estado 409 (conflicto) y un mensaje de error indicando que el nombre del producto ya está registrado. Esto evita que se creen productos duplicados en la base de datos.
 
    db_product = Product(name = product.name, category= product.category, price=product.price, quantity=product.quantity)
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

# Mostrar todos los productos
@app.get("/product"
         , response_model=list[Product], 
         status_code=status.HTTP_200_OK, 
         summary="Mostrar todos los productos")
def get_products(session: SessionDep):
    products = session.exec(
        select(Product)
    ).all()

    return products

# Eliminar un producto por su ID
@app.delete('/product/{id}',
            status_code=status.HTTP_200_OK,
    summary="Eliminar un producto por su ID"
)
def delete_product(product_id: int, session: SessionDep):
    product = session.exec(
            select(Product).where(Product.id == product_id)
    ).one()
    session.delete(product)
    session.commit()