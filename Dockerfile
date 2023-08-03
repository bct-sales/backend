FROM python:3.11-alpine AS base

ENV POETRY_VERSION=1.5.1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app


FROM base AS builder

RUN apk add --no-cache gcc
RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY . .
RUN poetry build


FROM base AS final
EXPOSE 8000

COPY --from=builder /app/dist/*.whl .
RUN pip install *.whl

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "backend.app:app" ]
