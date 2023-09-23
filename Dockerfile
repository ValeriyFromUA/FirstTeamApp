FROM python:3.8.0-slim
LABEL maintainer="Valerii Vasylenko<hitehnik132@gmail.com>"

COPY . /
WORKDIR /
COPY poetry.lock pyproject.toml ./


# Встановлюємо Poetry та залежності, а також uvicorn
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install
CMD python3 run.py