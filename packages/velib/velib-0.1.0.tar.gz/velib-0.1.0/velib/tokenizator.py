import jwt
from datetime import datetime, timedelta
import os



ALGORITHM = "HS256"
access_token_jwt_subject = "access"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = os.environ.get('SECRET_KEY', 'IuwYbM64l3wadqe3EKoyq9QgygrdjCCC');

def create_token(user_id: int, email: str = None, username: str = None) -> dict:
    """
    
    :param user_uid:
    :type user_uid:
    :param username:
    :type username:
    :param email:
    :type email:
    :return: JWT Token
    :rtype: dict
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires2 = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"id": user_id, "email": email}, expires_delta=access_token_expires
        )
    refresh_token = create_access_token(
            data={"id": user_id}
        )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_expire": datetime.timestamp(access_token_expires2)
    }


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    
    :param data:
    :type data:
    :param expires_delta:
    :type expires_delta:
    :return: token
    :rtype: string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    """
    
    :param token:
    :type token:
    :return: user uuid
    :rtype: str
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['id']
    except (Exception, jwt.exceptions.ExpiredSignatureError) as error:
        raise Exception(error)
    
    