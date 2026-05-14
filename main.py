from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from mongodb import words_collection
from bson import ObjectId

app = FastAPI(title="Словник MongoDB API")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, user_role: str = "user"):
    # Отримуємо дані з MongoDB
    words_cursor = words_collection.find()
    words = []
    for word in words_cursor:
        word['id'] = str(word['_id'])
        words.append(word)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"words": words, "role": user_role}
    )


@app.post("/add")
def add_word(word_text: str = Form(...), translation: str = Form(...), user_role: str = "admin"):
    # Додавання документа в MongoDB
    new_word = {"word_text": word_text, "translation": translation}
    words_collection.insert_one(new_word)
    return RedirectResponse(url=f"/?user_role={user_role}", status_code=303)


@app.get("/delete/{word_id}")
def delete_word(word_id: str, user_role: str = "admin"):
    # Видалення за ObjectId
    words_collection.delete_one({"_id": ObjectId(word_id)})
    return RedirectResponse(url=f"/?user_role={user_role}", status_code=303)

@app.post("/update/{word_id}")
def update_word(word_id: str, new_translation: str = Form(...), user_role: str = "admin"):
    words_collection.update_one(
        {"_id": ObjectId(word_id)},
        {"$set": {"translation": new_translation}}
    )
    return RedirectResponse(url=f"/?user_role={user_role}", status_code=303)


@app.get("/stats")
def get_stats():
    count = words_collection.count_documents({})
    return {
        "total_documents_in_mongodb": count,
        "database_name": words_collection.database.name,
        "collection_name": words_collection.name
    }

@app.get("/search")
def search_word(q: str):
    results = list(words_collection.find({"word_text": {"$regex": q, "$options": "i"}}))

    output = []
    for res in results:
        res['id'] = str(res['_id'])
        del res['_id']
        output.append(res)

    return {"search_query": q, "results": output}