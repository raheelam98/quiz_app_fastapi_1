
from quiz_backend.setting import access_expiry_time, refresh_expiry_time
from quiz_backend.models.user_models import User, UserModel, Token
from quiz_backend.controllers.auth_controllers import  (verifyPassword, passswordIntoHash, 
                                                         generateAccessAndRefreshToken,  decodeToken) # generateToken
from quiz_backend.utils.exception import (ConflictException, NotFoundException, InvalidInputException)

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, select
# Expiry things 

auth_schema = OAuth2PasswordBearer(tokenUrl="")
# check :- comes with bearer-token and 

# sign_in :- need user name, email and password 
# sign_in :- email and password both or any one exist choice another email or password
# login_in :-

def signUpFn(user_form: UserModel, session: Session):
    users = session.exec(select(User))

# authenticate, email and password is already exist in Database   
    for user in users:
        is_email_exist = user.user_email == user_form.user_email
        is_password_exit = verifyPassword(
            user.user_password, user_form.user_password
        )
        if is_email_exist and is_password_exit:
            raise ConflictException("email and password")
        if is_email_exist:
            raise ConflictException("email")
        if is_password_exit:
            raise ConflictException("password")

    hashed_password = passswordIntoHash(user_form.user_password) 

    user = User(user_name=user_form.user_name,
                user_email=user_form.user_email,
                user_password=hashed_password)   

    session.add(user)   
    session.commit()
    session.refresh(user)

    # generate access-token and refresh-token
    data = {
        "user_name" : user.user_name,
        "user_password": user.user_email,
        "access_expiry_time" : access_expiry_time,
        "refresh_expiry_time" : refresh_expiry_time
    }
    
    # destructure
    #access_token, refresh_token = generateAccessAndRefreshToken(data)

    token_data = generateAccessAndRefreshToken(data)
    
   # save refresh token in database
    token = Token(user_id=user.user_id, refresh_token= token_data["refresh_token"]["token"])
    
    session.add(token)
    session.commit()
    return token_data

# login controller (to fill the form require email and password)

def loginFn(login_form : OAuth2PasswordRequestForm, session: Session):
    # OAuth2PasswordRequestForm :- (1)restrict data into form-data and (2) require user-name and user-password
   
    users = session.exec(select(User))  # get all the users

    # loop for verifying each and ever useer
    for user in users:
        user_email = user.user_email    # check user-email exist
       
        # call verifyPassword fun:- verify user-password match with db password return bool
        verify_password = verifyPassword(user.user_password, login_form.user_password)

         # Check if provided credentials are valid
        if user_email == login_form.username and verify_password:

                    # generate access-token and refresh-token
            data = {
                    "user_name" : user.user_name,
                    "user_password": user.user_email,
                    "access_expiry_time" : access_expiry_time,
                    "refresh_expiry_time" : refresh_expiry_time
                    }
    
            token_data = generateAccessAndRefreshToken(data)
                
            # Update the refresh token in the database 
            token = session.exec(select(Token).where(Token.user_id == user.user_id)).one()
            token.refresh_token = token_data["refresh_token"]["token"]
    
            session.add(token)
            session.commit()
            session.refresh(token)
            return token_data
        
        # if processs is fail, else throw error message
        else:
             raise InvalidInputException("Email or Password")
        

    # note :- login()
    #user-form, select user and check user already exist
    # if user exist authorize, otherwise give invalid exception
    # varify user email and then convert password (unhashable) and varify
        

# get-user (base on token) auth provide all related things of token (use bearer token) (time 25)
def getUsersFn(token: Annotated[str, Depends(auth_schema)], session: Session):
    """
    Function to get user details using an access token.
    Args:
        token (str): The access token.
        session (Session): The database session.
    Returns:
        User: The user object.
    """
    try:
        if token:
            data = decodeToken(token)

            # dict.keys() :- returns a list of all the available keys in the dictionary
            user_email = data["user_email"]
            # select user structure
            user = session.exec(select(User).where(User.user_email == user_email)).one()
            return user
    except :
        raise NotFoundException("Token")


     
         
# through jwt decode token
# one() : only return one thing if get more or nothing it give error ???
# first() :- give the only first value but doesn't give error ???
