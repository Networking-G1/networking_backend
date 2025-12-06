# database.py
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Construye la URL. 
# Es mejor construirla parte por parte o asegurar que DATABASE_URL exista.
# Nota el cambio a "postgresql+psycopg2"
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No se encontró la variable DATABASE_URL en el archivo .env")

# Reemplaza postgres:// por postgresql+psycopg2:// si Supabase te da el formato antiguo
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

# echo=True es útil para ver los SQL que se ejecutan mientras desarrollas
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # Las tablas ya existen en Supabase, no crear
    pass

def get_session():
    with Session(engine) as session:
        yield session