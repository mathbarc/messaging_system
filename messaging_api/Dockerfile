from python:3.11.2-slim as build

RUN apt update -y
RUN apt install build-essential -y
RUN pip install pipenv

COPY ./ ./

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

from python:3.11.2-slim as runtime

COPY --from=build ./.venv/ /venv/
ENV PATH="/venv/bin:$PATH"

ENTRYPOINT [ "bash" ]