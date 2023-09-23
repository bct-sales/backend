#! /usr/bin/env bash

cd src
poetry run uvicorn backend.app:app --reload
