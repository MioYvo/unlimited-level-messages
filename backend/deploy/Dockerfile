FROM python:3.10-slim

COPY deploy/cn-sources.list /etc/apt/sources.list
COPY deploy/requirements.txt /app/requirements.txt

RUN apt update && \
    pip install -r /app/requirements.txt && \
    # [imp] Need to change backend/deploy/data ownership when REAL production deploy
#    chown -R nobody:nogroup /app && \
#    mkdir /data && chown -R nobody:nogroup /data && \
    apt autoremove && apt clean

COPY flaskr /app/flaskr
WORKDIR /app
#USER nobody

CMD ["gunicorn", "--preload", "-w", "4", "-b", "0.0.0.0:5000", "flaskr:create_app()"]
