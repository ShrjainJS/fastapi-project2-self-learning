from fastapi import FastAPI, Body, Path, Query, HTTPException
from models.book_model import BookRequest
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

BOOKS = [
    Book(1, 'Title One', "Author One", "Desc One", 5, 2012),
    Book(2, 'Title Two', "Author Two", "Desc Two", 4, 2014),
    Book(3, 'Title Three', "Author Three", "Desc Three", 3, 2022),
    Book(4, 'Title Four', "Author One", "Desc Four", 5, 2025),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="Item Not Found.")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(gt=0, le=5)):
    return_list = []
    for book in BOOKS:
        if book.rating == int(rating):
            return_list.append(book)
    return return_list

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_book_by_publish_year(published_year:int = Query(gt=0)):
    return_list = []
    for book in BOOKS:
        if book.published_year == published_year:
            return_list.append(book)
    return return_list
    

@app.put("/books/update_book", status_code = status.HTTP_204_NO_CONTENT)
async def update_book(book_body: BookRequest):
    book_body_updated = Book(**book_body.model_dump())
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_body_updated.id:
            BOOKS[i] = book_body_updated
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail='Book Not Found.')

@app.post("/books/add", status_code=status.HTTP_201_CREATED)
async def add_new_book(book_to_add = Body()):
    id_to_add = len(BOOKS) + 1
    title_to_add = book_to_add.get("title").casefold().title()
    author_to_add = book_to_add.get("author").casefold().title()
    desc_to_add = book_to_add.get("description").casefold().title()
    rating_to_add = int(str(book_to_add.get("rating")))
    published_year_to_add = int(book_to_add.get("published_year"))

    BOOKS.append(
        Book(id_to_add, title_to_add, author_to_add, desc_to_add, rating_to_add, published_year_to_add)
    )

@app.post("/book/add/v2", status_code=status.HTTP_201_CREATED)
async def create_new_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book : Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found.')

