from datetime import datetime, timedelta
from typing import Optional
from backend.security.scopes import Scope
from backend.settings import load_settings
from jose import jwt


class TokenData:
    __email_address: str

    __scopes: set[Scope]

    def __init__(self, email_address: str, scopes: set[Scope]):
        self.__email_address = email_address
        self.__scopes = scopes

    @property
    def email_address(self) -> str:
        return self.__email_address

    @property
    def scopes(self) -> set[Scope]:
        return self.__scopes


def _compute_expiration_date(duration: Optional[timedelta]) -> datetime:
    now = datetime.utcnow()
    settings = load_settings()
    duration = duration if duration else timedelta(minutes=settings.jwt_expiration)
    return now + duration


def create_access_token(*, token_data: TokenData, duration: Optional[timedelta] = None) -> str:
    settings = load_settings()
    expiration_date = _compute_expiration_date(duration)
    secret_key = settings.jwt_secret_key
    algorithm = settings.jwt_algorithm
    claims = {
        'sub': token_data.email_address,
        'exp': expiration_date,
        'scopes': [scope.name for scope in token_data.scopes],
    }
    return jwt.encode(claims=claims, key=secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> Optional[TokenData]:
    settings = load_settings()
    secret_key = settings.jwt_secret_key
    algorithm = settings.jwt_algorithm
    try:
        data = jwt.decode(token=token, key=secret_key, algorithms=[algorithm])
        email_address = data['sub']
        scopes = {Scope.from_name(name) for name in data['scopes']}
        return TokenData(email_address=email_address, scopes=scopes)
    except:
        return None
