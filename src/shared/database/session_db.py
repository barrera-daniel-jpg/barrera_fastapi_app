from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno.")

engine = create_engine(database_url)

# Crea el motor de la base de datos
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
