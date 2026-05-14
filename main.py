from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
import psycopg2
from database import engine, get_db

app = FastAPI(
    title="Словник-Перекладач API",
    description="Лабораторна робота №1: API для керування словником слів",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Слова",
            "description": "Операції зі словами у словнику",
        }
    ]
)
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

# Головна сторінка зі списком слів
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db), user_role: str = "user"):
    words = db.query(models.Word).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"words": words, "role": user_role}
    )

# Ендпоінт для додавання слова (Create)
@app.post("/add")
def add_word(word_text: str = Form(...), translation: str = Form(...), db: Session = Depends(get_db), user_role: str = "user"):
    new_word = models.Word(word_text=word_text, translation=translation)
    db.add(new_word)
    db.commit()
    return RedirectResponse(url=f"/?user_role={user_role}", status_code=303)

@app.post("/update/{word_id}")
def update_word(word_id: int, new_translation: str = Form(...), db: Session = Depends(get_db), user_role: str = "user"):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if word:
        word.translation = new_translation
        db.commit()
    return RedirectResponse(url=f"/?user_role={user_role}", status_code=303)

@app.get("/delete/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db), user_role: str = "user"):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if word:
        db.delete(word)
        db.commit()
    return RedirectResponse(url=f"/?user_role={user_role}", status_code=303)

@app.get("/stats")
def get_stats():
    # Пряме підключення через psycopg2
    conn = psycopg2.connect(
        dbname="dictionary_db",
        user="postgres",
        password="170806vK",
        host="localhost"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM words")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_words_in_db": count}


@app.get("/init-languages")
def init_languages():
    # Використовуємо psycopg2 для масового додавання даних (executemany)
    conn = psycopg2.connect(dbname="dictionary_db", user="postgres", password="170806vK", host="localhost")
    cursor = conn.cursor()

    languages = [('English',), ('Ukrainian',), ('German',)]

    cursor.executemany("INSERT INTO languages (name) VALUES (%s) ON CONFLICT DO NOTHING", languages)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Мови успішно ініціалізовано в PostgreSQL через Psycopg2"}