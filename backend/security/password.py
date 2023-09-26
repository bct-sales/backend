from passlib.context import CryptContext


_pwd_cxt = CryptContext(
   schemes=["bcrypt"],
   deprecated="auto"
)


def hash_password(password: str) -> str:
   return _pwd_cxt.hash(password)


def verify_password(*, hash: str, plaintext: str):
      return _pwd_cxt.verify(plaintext, hash)


def is_valid_password(password: str) -> bool:
     return len(password) >= 2
