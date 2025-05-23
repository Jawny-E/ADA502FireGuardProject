##### build stage #####
FROM python:3.12 AS builder

WORKDIR /app 

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add project-files and build the poetry-package
COPY API/ .
WORKDIR /app/API

RUN /root/.local/bin/poetry install
RUN /root/.local/bin/poetry build

##### compile stage #####
FROM python:3.12-alpine

# Add curl here in root context
USER root
RUN apk update && apk add --no-cache curl

RUN addgroup -g 1000 app && adduser -G app -D -u 1000 -h /app app

WORKDIR /app
USER app
COPY --from=builder --chown=1000:1000 /app/dist .
RUN pip install fireguard_app-0.1.0-py3-none-any.whl
ENV PATH="/app/.local/bin:${PATH}"
EXPOSE 8000
ENTRYPOINT ["uvicorn", "fireguard_app.app:app", "--host", "0.0.0.0", "--port", "8000"]
