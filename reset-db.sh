#! /usr/bin/env bash

export BCT_DATABASE_PATH=G:/repos/bct/backend/bct.db

rm $BCT_DATABASE_PATH

cd src

poetry run py createdb.py
