from . import user
from ..models import User
from flask import request
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from ..models import Book

@user.get("/user")
@jwt_required()
def get_user(): 
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).one_or_none()

    if user is None:
        response = {
            "message": "please create an account before trying to login"
        }
        return response, 400


    books = Book.query.filter_by(user_id  = current_user_id).all()
    response = {
        "username": user.username,
         "books": [book.to_response() for book in books] 
    }

    return response , 200