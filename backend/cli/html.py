from backend import settings
import click
from pathlib import Path


@click.group
def html():
    pass


@html.command(help='Downloads latest html')
@click.argument('location', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def download(location: str):
    import urllib.request
    cfg = settings.load_settings(verify=False)
    url = cfg.html_url
    print(f'Downloading {url}')
    with urllib.request.urlopen(url) as stream:
        data = stream.read()
    path = Path(location) / 'index.html'
    print(f'Writing {path}')
    with open(path, 'wb') as file:
        file.write(data)
    print("Make sure to set BCT_HTML_PATH if you want to serve this HTML file")
