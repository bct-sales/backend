from datetime import datetime, timedelta
from typing import Optional
from backend.security.scopes import Scope, Scopes
from backend.settings import load_settings
from jose import jwt


class TokenData:
    __user_id: int

    __scopes: Scopes

    def __init__(self, user_id: int, scopes: Scopes):
        self.__user_id = user_id
        self.__scopes = scopes

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def scopes(self) -> Scopes:
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
        'sub': str(token_data.user_id),
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
        user_id = int(data['sub'])
        scopes = Scopes(*(Scope.from_name(name) for name in data['scopes']))
        return TokenData(user_id=user_id, scopes=scopes)
    except:
        return None
