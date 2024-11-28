from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#  pip install passlib
# pip install bcrypt - where schemes = ["bcrypt"]
#  pip install argon2-cffi

# hashing is used to hide the password - means it encodes the password and we won't get the original password back

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
