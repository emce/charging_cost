# Zaptec charging cost

![alt text](./static/img/charging_logo.svg)

Django application to show charging costs based on set tariff and data from Zaptec API

## Instalation

In order to install application locally, run:

`git clone https://github.com/emce/charging_cost`

`cd charging_cost`

`pip3 install -r requirements.txt`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py runserver`

... and open: `http://localhost:8000`

## Docker

Application can be deployed and run as docker image with compose plugin:

```yaml
version: '3'
services:
  web:
    container_name: charging_stats
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env
    ports:
      - "9080:9080"
    volumes:
      - ./:/code
    command: sh ./entrypoint.sh
    networks:
      - outside

  nginx:
    build: ./nginx
    ports:
      - "9081:9081"
    restart: always
    volumes:
      - ./:/code
    depends_on:
      - web
    networks:
      - outside

volumes:
  static:
```