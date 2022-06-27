FROM python:alpine

LABEL maintainer twtrubiks

# Get latest root certificates
RUN apk add --no-cache ca-certificates tzdata && update-ca-certificates

# Install the required packages
RUN pip install --no-cache-dir flower==1.0.0 Django==4.0.5 django-bootstrap3==21.2 django-celery-results==2.3.1 requests==2.28.0

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
# PYTHONDONTWRITEBYTECODE: Do not write byte files to disk, since we maintain it as readonly. (equivalent to `python -B`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1

# Default port
EXPOSE 5555

ENV FLOWER_DATA_DIR /data
ENV PYTHONPATH ${FLOWER_DATA_DIR}

WORKDIR $FLOWER_DATA_DIR

# Add a user with an explicit UID/GID and create necessary directories
RUN set -eux; \
    addgroup -g 1000 flower; \
    adduser -u 1000 -G flower flower -D; \
    mkdir -p "$FLOWER_DATA_DIR"; \
    chown flower:flower "$FLOWER_DATA_DIR"
USER flower

VOLUME $FLOWER_DATA_DIR

CMD ["celery", "flower"]
