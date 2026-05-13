from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Назва файлу бази даних, який автоматично створиться
SQLALCHEMY_DATABASE_URL = "sqlite:///./dictionary.db"

# Створення рушія для SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Створення фабрики сесій для роботи з БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для наших майбутніх таблиць
Base = declarative_base()

# Функція для отримання доступу до БД у наших маршрутах (ендпоінтах)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()