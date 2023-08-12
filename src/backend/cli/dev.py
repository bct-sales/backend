from backend.cli.database import get_database
from backend.security import roles
from backend.security.tokens import create_access_token, TokenData
import datetime
import click
import sys


@click.group
def dev():
    pass


@dev.command
@click.argument('email')
def genauth(email):
    database = get_database()
    with database.session as session:
        user = session.find_user_with_email_address(email_address=email)

    if user is None:
        print(f'Error: no user found with email address {user}')
        sys.exit(-1)

    role = roles.Role.from_name(user.role)
    token_data = TokenData(user_id=user.user_id, scopes=role.scopes)
    access_token = create_access_token(token_data=token_data, duration=datetime.timedelta(days=365))
    print(f'''
const accessToken = `{access_token}`;
const emailAddress = `{email}`;
const role = '{role.name}';
const userId = {user.user_id};
          '''.strip())
