from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
import schema

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "039rhfj4994yrcbrt74r47rt7cgrt847r982927847743rtgc98y47n"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 45

# Login access for registered user
def access_token(data: dict):
    to_encode = data.copy()

    expireIn = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expireIn})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schema.Token(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

# Verify a user if logged in before they can perform any action
def get_current_user(token : Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials!", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)