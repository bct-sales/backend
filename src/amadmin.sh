#! /usr/bin/env bash

export BCT_DATABASE_PATH=~/bct.db
export BCT_HTML_PATH=~/index.html
export BCT_LABEL_GENERATION_DIRECTORY=~/labels

poetry run python admin.py $@
