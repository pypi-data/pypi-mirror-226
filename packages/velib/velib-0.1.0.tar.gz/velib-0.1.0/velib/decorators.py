from functools import wraps
from fastapi import HTTPException, Header
from fastapi.requests import Request
import jwt
import os


SECRET_KEY = os.environ.get('SECRET_KEY', 'IuwYbM64l3wadqe3EKoyq9QgygrdjCCC');

CONTENT_TYPE = 'application/json'


def authorize(request: Request):
    if 'Authorization' not in request.headers:
        raise HTTPException(status_code=401, detail='Unauthorized')

    data = request.headers['Authorization']
    token = str.replace(str(data), 'Bearer ', '')
    
    try:
        user_id = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['id']
    except (Exception, jwt.exceptions.ExpiredSignatureError) as error:
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        return user_id


def content_type(request: Request):
    content_type_header = request.headers.get('Content-Type')
    if content_type_header != CONTENT_TYPE:
        raise HTTPException(status_code=400, detail="Content-Type header invalid")

