from . import book
from flask import request
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from ..models import Book



@book.post("/new")
@jwt_required()
def handle_create_book():
    body = request.json

    if body is None:
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    title = body.get("title")
    if title is None or title == "":
        response = {
            "message": "invalid request"
        }
        return response, 400

    author = body.get("author")
    if author is None or author == "":
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    genre = body.get("genre")
    if genre is None or author == "":
        response = {
            "message": "invalid request"
        }
        return response, 400

    existing_book = Book.query.filter_by(title=title).one_or_none()
    if existing_book is not None:
        response = {
            "message": "that title is already in use"
        }
        return response, 400

    book = Book(title=title, author=author, genre=genre,  user_id=current_user.id)
    book.create()

    response = {
        "message": "successfully created book",
        "book": book.to_response()
    }
    return response, 201

@book.get("/all")
@jwt_required()
def handle_get_all_books():
    books = Book.query.all()
    response = {
        "message": "book retrieved",
        "books": [book.to_response() for book in books]
    }
    return response, 200

@book.get("/mine")
@jwt_required()
def handle_get_my_books():
    books = Book.query.filter_by(created_by=current_user.id).all()
    response = {
        "message": "books retrieved",
        "books": [book.to_response() for book in books]  
    }
    return response, 200


@book.get("/book/<book_id>")
@jwt_required()
def handle_get_one_book(book_id):
    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            "message": "book does not exist"
        }
        return response, 404

    response = {
        "message": "book found",
        "book": book.to_response() 
    }
    return response, 200

@book.delete("/delete_book/<book_id>")
@jwt_required()
def handle_delete_book(book_id):
    
    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            "message": "book does not exist"
        }
        return response, 404

    current_user = get_jwt_identity()
    if book.user_id != current_user:
        response = {
            "message":"you cant delete someone elses quiz"
        }
        return response, 401
    
    book.delete()

    response = {
        "message": f"book {book.id} deleted"
    }
    return response, 200

@book.put("/update_book/<book_id>")
@jwt_required()
def handle_update_book(book_id):
    
    body = request.json
    

    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            "message": "not found"
        }
        return response, 404

    current_user_id = get_jwt_identity()
    if book.user_id != current_user_id:
        response = {"message":"no sir/maam"}
        return response, 401
    
   
   
    book.title = body.get("title", book.title)
    book.author = body.get("author", book.author)
    book.genre= body.get("genre", book.genre)
    
    book.update()

    response = {
        "message": "book updated",
        "book": book.to_response()
    }
    return response, 200