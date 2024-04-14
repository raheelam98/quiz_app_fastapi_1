from starlette.config import Config
from datetime  import timedelta
#from quiz_backend.utils.imports import timedelta


# Initialize config object with path to .env file
try:
    config = Config(".env")
except FileNotFoundError as e:
    print(e)

# get database URLs from config object   
db_url = config.get("DB_URL")

#test_db_url  = config.get("TEST_DB_URL ")

# access_expiry_time = config.get("ACCESS_EXPIRY_TIME")
# refresh_expiry_time = config.get("REFRESH_EXPIRY_TIME")

# SECRET_KEY = config("SECRET_KEY", cast=str)
# ALGORITHM = config("ALGORITHM", cast=str)

# set time for token
access_expiry_time = timedelta(minutes=int(config.get("ACCESS_EXPIRY_TIME")))  
refresh_expiry_time = timedelta(days=int(config.get("REFRESH_EXPIRY_TIME")))

secret_key = config.get("SECRET_KEY")

algorithm = config.get("ALGORITHM")

# check note :- anything store in eng is str, here convert into int
# timedelta() :- object represents a duration, the difference between two datetime 
# class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)



