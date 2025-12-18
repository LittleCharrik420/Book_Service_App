from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
import os

from database import engine, Base
from routes import books, users, bookmarks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Service API",
    description="API для книжного сервиса",
    version="1.0.0"
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(bookmarks.router)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Главная страница - каталог книг"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/book/{book_id}", response_class=HTMLResponse)
def book_detail(request: Request, book_id: int):
    """Страница отдельной книги"""
    return templates.TemplateResponse("book_detail.html", {
        "request": request,
        "book_id": book_id
    })

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Страница регистрации"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Страница входа"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    """Страница профиля"""
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/bookmarks", response_class=HTMLResponse)
def bookmarks_page(request: Request):
    """Страница закладок"""
    return templates.TemplateResponse("bookmarks.html", {"request": request})

@app.get("/health")
def health_check():
    """Проверка здоровья приложения"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
