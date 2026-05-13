from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Таблиця користувачів (Ролі: 'admin' або 'user')
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String, default="user") # 'admin' або 'user'

# Таблиця мов (наприклад: English, Ukrainian)
class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True) # Назва мови

# Таблиця слів та їх перекладів
class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word_text = Column(String, index=True)     # Слово мовою оригіналу
    translation = Column(String)               # Переклад
    language_id = Column(Integer, ForeignKey("languages.id"))

    # Зв'язок: кожне слово належить до конкретної мови
    language = relationship("Language")