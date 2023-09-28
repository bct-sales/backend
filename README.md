# Readme

## Installation Instructions

* `apt update`
* `apt install python3 python3-pip emacs nginx pkg-config libcairo2-dev`
* Clone this repository
* Inside repo, `poetry install`.
* Also under `/backend``, create `.env` file (see below for contents).
* Download html using `./download-html.sh`.
* Might have to change owner of `/var/www/html` to user `www-data`: in `/`, `sudo chown -R www-data var/www/html`
* Configure `nginx` by `sudo cp ./ngingx-config /etc/nginx/sites-enabled/fastapi_nginx`.
* Restart `nginx` using `sudo service nginx restart`.
* Back in home directory, clone bctqr.
* Inside repo, `poetry install`.
* Make directory `~/labels`
* Run server process: in `backend`, run `./start-prod.sh`.

## .venv

Use `generate-jwt-key.sh` script to generate `BCT_JWT_SECRET_KEY`.

```bash
BCT_JWT_SECRET_KEY=???
BCT_DATABASE_PATH=~/bct.db
BCT_HTML_PATH=~/index.html
BCT_LABEL_GENERATION_DIRECTORY=~/labels
BCT_QR_DIRECTORY=~/bctqr
```

## Technologies

* Python
* FastAPI
* Poetry
* Pydantic
* SQLAlchemy
* SQLite
