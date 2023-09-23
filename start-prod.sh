#! /usr/bin/env bash

cd src
poetry run uvicorn backend.app:app --host 0.0.0.0 --port 80
