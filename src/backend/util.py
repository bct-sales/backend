from fastapi import Request


def url_for(request: Request, name: str, **kwargs) -> str:
    url = str(request.url_for(name, **kwargs))
    # TODO Ugly solution for tricky issue
    # url = url.replace('http://127.0.0.1:8000', '')
    return url
