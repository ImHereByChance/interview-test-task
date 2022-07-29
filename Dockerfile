FROM python:3.8.13-buster

# installing poetry
ENV POETRY_HOME /.poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

ENV LANG C.UTF-8

COPY src src
COPY db .

# hardcoded for simplicity (usually it comes from CI variables or args)
RUN export APP_VERSION="0.0.1"

EXPOSE 8000
CMD ["poetry", "run", "python", "src"]