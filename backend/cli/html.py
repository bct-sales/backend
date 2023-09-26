from backend import settings
import click


@click.group
def html():
    pass


@html.command(help='Downloads latest html')
def download():
    import urllib.request
    cfg = settings.load_settings(verify=False)
    path = cfg.html_path
    url = cfg.html_url
    print(f'Downloading {url}')
    with urllib.request.urlopen(url) as stream:
        data = stream.read()
    print(f'Writing {path}')
    with open(path, 'wb') as file:
        file.write(data)
