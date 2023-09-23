from fastapi import Request


def url_for(request: Request, name: str, **kwargs) -> str:
    # TODO Ugly solution for tricky issue
    url = str(request.url_for(name, **kwargs))
    return url.replace('http://127.0.0.1:8000', '')
