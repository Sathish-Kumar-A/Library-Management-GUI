from library import Book
import json

def load_books():
    try:
        file=open("book.dat",'r')
        book_dict=json.loads(file.read())
        books=[]
        #id,name,description,isbn,page_count,issued,author,year
        for book in book_dict:
            book_obj=Book(book['id'],book['name'],book['description'],book['isbn'],book['page_count'],book['issued'],book['author'],book['year'])
            books.append(book_obj)
        return books
    except:
        return []

def save_books(books):
    json_books=[]
    for book in books:
        json_books.append(book.to_dict())
    with open("book.dat",'w')as file:
        file.write(json.dumps(json_books,indent=4))

def add_book(book):
    books=load_books()
    new_book=Book(book['id'],book['name'],book['description'],book['isbn'],book['page_count'],book['issued'],
                  book['author'],book['year'])
    save_books([*books,assign_idvalue(books,new_book)])

def assign_idvalue(books,new_book):
    book_ids=[]
    for book in books:
        book_ids.append(int(book.id))
    if list(filter(lambda id: id == int(new_book.id),book_ids))==[]:
        return new_book
    else:
        new_book.id=int(max(book_ids)+1)
        return new_book
def get_issuedbooks():
    books=load_books()
    for book in books:
        return list(filter(lambda book:book.issued==True,books))
def get_unissuedbooks():
    books=load_books()
    for book in books:
        return list(filter(lambda book:book.issued==False,books))
def find_books(book_id):
    books=load_books()
    for book in books:
        if book.id==book_id:
            return book
    return None
def update_book(book):
    book=Book(book['id'],book['name'],book['description'],book['isbn'],book['page_count'],book['issued'],
                  book['author'],book['year'])
    books=load_books()
    if book != None:
        books = list(filter(lambda bk: int(bk.id) != int(book.id), books))
        books.append(book)
        save_books(books)

def deletebook(id):
    books=load_books()
    books=list(filter(lambda bk: int(bk.id)!=int(id),books))
    save_books(books)

