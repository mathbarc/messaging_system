FROM debian:bookworm as base
RUN apt update -y
RUN apt install python3 python3-pip libmariadb3 -y


FROM base as build

RUN apt install build-essential libmariadb-dev mariadb-client pipenv -y

WORKDIR /home
COPY ./ ./

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install 


FROM base as runtime

COPY --from=build /home/.venv/ /home/.venv/
ENV PATH="/home/.venv/bin:$PATH"

ENTRYPOINT [ "messaging_api" ]