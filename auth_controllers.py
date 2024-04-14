from typing import Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from quiz_backend.setting import algorithm, secret_key
#from quiz_backend.utils.imports import timedelta
from quiz_backend.utils.types import TokenType
from datetime import timedelta


# encryption/decryption algorithms

# CryptContext class, which is used for securely hashing and verifying passwords
# bcrypt algorithm is commonly used for password hashing
pwd_context = CryptContext(schemes="bcrypt")   # instance of the CryptContext class

# token is provided on base of user data and expiry_time
# dynamic function to generate either access or refresh token, only change expiry_time 
# function generates a JWT (JSON Web Token) based on user data and an expiration time.
def generateToken(data, expiry_time : timedelta ):
    try:
        # create a copy of the data dictionary to avoid modifying the original data
        to_encode_data = data.copy()      # import all the data (copy data store in to_encode_data)
        
        # Add an "exp" (expiration) claim to the data dictionary
        to_encode_data.update({ "exp" : expiry_time })   # provide dict to update copy-data

        # encodes the data in to_encode_data into a JWT                                    
        # import data into jwt :- encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        token = jwt.encode(to_encode_data, secret_key, algorithm=algorithm)
        return token
    except JWTError as je:
        raise je

def generateAccessAndRefreshToken(user_details: dict[str, Any]):
    data = {
        "user_name": user_details["user_name"],
        "user_email": user_details["user_email"]
    }

    access_token = generateToken(data, user_details["access_expiry_time"])
    refresh_token = generateToken(data, user_details["refresh_expiry_time"])

    # convert time into seconds (Cookies save time in sec) (for route)
    access_expiry_time = user_details["access_expiry_time"].total_seconds()
    refresh_expiry_time = user_details["refresh_expiry_time"].total_seconds()
    
    # return dict
    return{
        "access_token": {
                        "token" :access_token,
                        "access_expiry_time": access_expiry_time
                        },
        "refresh_token": {
                        "token" :refresh_token,
                        "arefresh_expiry_time": refresh_expiry_time
                        }
          }

def decodeToken(token: str):
    """
    Decodes a JWT token to retrieve the payload data.
    Args:
        token (str): The JWT token to decode.
    Returns:
        dict: The decoded payload data.
    """
    try:
        # Decode the token to retrieve the payload data
        decoded_data = jwt.decode(token, secret_key, algorithms=algorithm)
        return decoded_data
    except JWTError as je:
        # Raise an exception if there's an error decoding the token
        raise je

    
# function convert user plain password into hash
def passswordIntoHash(plaintext: str):
    hashedpassword = pwd_context.hash(plaintext)
    return hashedpassword

def verifyPassword(hashPass: str, plaintext: str):
    verify_password = pwd_context.verify(plaintext, hash=hashPass)
    return verify_password
    

def tokenService():
    ...        

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=jwt#hash-and-verify-the-passwords
    
# note :- decode on basis of security key
# note :- openssl rand -hex 30  (generate random token)
# copy() method returns a copy of the DataFrame (deep-copy)
# Python timedelta():-  calculating differences in datetime objects
# Syntax : datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0) 
# Returns : Date  
# encode :- convert into a coded form  
