#! /usr/bin/env bash

export BCT_DATABASE_PATH=G:/repos/bct/backend/bct.db

cd src
poetry run uvicorn backend.app:app --reload
