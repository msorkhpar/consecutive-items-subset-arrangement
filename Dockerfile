FROM python:3.10-slim-bullseye AS python-deps

RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM python:3.10-slim-bullseye AS runtime
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
WORKDIR /app

COPY main.py .
COPY generators/ ./generators/
COPY lp/ ./lp/
COPY transformers/ ./transformers/
COPY utils/ ./utils/

CMD ["python", "main.py"]
