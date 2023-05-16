FROM python:3.10-slim-bullseye

RUN pip install --upgrade pip
RUN pip install pipenv
WORKDIR /app

COPY main.py /app/main.py
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
COPY generators/ /app/generators
COPY utils/ /app/utils

RUN pipenv install --system --deploy

CMD ["python", "main.py"]
