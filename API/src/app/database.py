from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class DatabaseConfig:
    """Clase para manejar la configuración de la base de datos."""
    def __init__(self):
        self.host = os.getenv("DATABASE_HOST")
        self.port = os.getenv("DATABASE_PORT")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.db_name = os.getenv("DATABASE_NAME")

    def get_database(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

# Configuración de la base de datos
db_config = DatabaseConfig()

# Crear el motor de base de datos
engine = create_engine(db_config.get_database())

# Crear una clase base de modelo declarativo
Base = declarative_base()

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()