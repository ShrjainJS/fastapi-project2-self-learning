from fastapi import FastAPI, Body
from models.book_model import BookRequest

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(1, 'Title One', "Author One", "Desc One", 5),
    Book(2, 'Title Two', "Author Two", "Desc Two", 4),
    Book(3, 'Title Three', "Author Three", "Desc Three", 3),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/books/add")
async def add_new_book(book_to_add = Body()):
    id_to_add = len(BOOKS) + 1
    title_to_add = book_to_add.get("title").casefold().title()
    author_to_add = book_to_add.get("author").casefold().title()
    desc_to_add = book_to_add.get("description").casefold().title()
    rating_to_add = int(str(book_to_add.get("rating")))

    BOOKS.append(
        Book(id_to_add, title_to_add, author_to_add, desc_to_add, rating_to_add)
    )

@app.post("/book/add/v2")
async def create_new_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book : Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
    