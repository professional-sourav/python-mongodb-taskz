from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = '123456abc#'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'])

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except JWTError:
        return None
