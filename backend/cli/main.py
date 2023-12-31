from backend.cli.database import get_database
from backend.db import models
from backend.security import roles
from backend.security.tokens import create_access_token, TokenData
from backend.cli.dev import dev
from backend.cli.database import db
from backend.cli.settings import settings
from backend.cli.html import html
import datetime
import click


@click.group()
def cli():
    pass


cli.add_command(db)
cli.add_command(dev)
cli.add_command(settings)
cli.add_command(html)
