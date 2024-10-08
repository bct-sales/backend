# Readme

## Installation Instructions

* `sudo apt update`
* `sudo apt install python3 python3-pip emacs nginx pkg-config libcairo2-dev`
* Clone this repository
* Inside repo, `poetry install`.
* Also under `/backend`, create `.env` file (see below for contents).
* Download html using `./download-html.sh`.
* Might have to change owner of `/var/www/html` to user `www-data`: in `/`, `sudo chown -R www-data var/www/html`
* Configure `nginx` by `sudo cp ./ngingx-config /etc/nginx/sites-enabled/fastapi_nginx`.
* Restart `nginx` using `sudo service nginx restart`.
* Back in home directory, clone bctqr.
* Inside repo, `poetry install`.
* Make directory `~/labels`.
* Make directory `~/backups`.
* If necessary, create new database.
  * In home directory, run `sqlite3 bct.db ""`.
  * In `backend`, run `./admin.sh db reset` to populate it with tables.
  * Create the necessary users.
* Run server process: in `backend`, run `nohup ./start-prod.sh &`.

## Shutting Down Server

* Enter `ps -A`.
* Look of `uvicorn` and get process ID.
* Send SIGINT message using `kill -2 ID`.

## .env

In a `.env` file, add

```bash
BCT_JWT_SECRET_KEY=???
BCT_DATABASE_PATH=~/bct.db
BCT_DB_BACKUP_DIRECTORY=~/backups
BCT_LABEL_GENERATION_DIRECTORY=~/labels
BCT_QR_DIRECTORY=~/bctqr
```

Use `generate-jwt-key.sh` script to generate `BCT_JWT_SECRET_KEY`.

## DB Backup

Inside `backend`, use `./admin.sh db backup`.
It will copy the database to `BCT_DB_BACKUP_DIRECTORY`.
It can run while the server is running.

## Shell Screens

Start with `screen`.

* `ctrl+a c` creates new screen (shell).
* `ctrl+a "` gives list of screens.

## Technologies

* Python
* FastAPI
* Poetry
* Pydantic
* SQLAlchemy
* SQLite
