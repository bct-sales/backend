import click


@click.group
def settings():
    pass


@settings.command(help='Generates a .env file template')
def gendotenv():
    with open('.env', 'w') as file:
        print("BCT_JWT_SECRET_KEY=", file=file)
        print("BCT_DATABASE_PATH=", file=file)
        print("BCT_DB_BACKUP_DIRECTORY=", file=file)
        print("BCT_LABEL_GENERATION_DIRECTORY=", file=file)
        print("BCT_QR_DIRECTORY=", file=file)
        
