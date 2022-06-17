FROM python:3.10-slim

COPY deploy/cn-sources.list /etc/apt/sources.list
COPY deploy/requirements-dev.txt /app/requirements.txt
COPY setup.py setup.cfg /app/
WORKDIR /app

RUN apt update && \
    pip install -r /app/requirements.txt && \
    pip install -e . && \
    # [imp] Need to change backend/deploy/data ownership when REAL production deploy
#    chown -R nobody:nogroup /app && \
#    mkdir /data && chown -R nobody:nogroup /data && \
    apt autoremove && apt clean

COPY flaskr /app/flaskr
COPY tests /app/tests
#USER nobody

CMD ["pytest"]
