#! /usr/bin/env bash

export BCT_DATABASE_PATH=G:/repos/bct/backend/bct.db
export BCT_HTML_PATH=G:/repos/bct/frontend/dist/index.html
export BCT_LABEL_GENERATION_DIRECTORY=G:/temp

cd src
poetry run uvicorn backend.app:app --reload
