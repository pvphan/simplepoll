FROM python:3.11.4-bullseye
RUN python3 -m pip install Flask==2.3.2 pandas==2.0.3
WORKDIR /simplepoll
