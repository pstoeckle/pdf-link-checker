# SPDX-FileCopyrightText: 2023 Siemens AG, Patrick Stoeckle, and other contributors.
# SPDX-License-Identifier: LicenseRef-Siemens-ISL-1.4
# syntax=docker/dockerfile:1.3

FROM python:3.11.3-slim-bullseye as base

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ARG http_proxy
ARG https_proxy
ARG no_proxy

RUN pip install -q --no-cache-dir --upgrade pip==23.1.2

FROM base as test

RUN useradd --create-home --shell /bin/bash poetry-user

WORKDIR /home/poetry-user
USER poetry-user
ENV PATH="/home/poetry-user/.local/bin:$PATH"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update -qq \
    && apt-get install --no-install-recommends -qqy \
    curl=7.74.0-1.3+deb11u7 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists \
    && ( curl -sSL https://install.python-poetry.org | python3 - --version 1.4.1) \
    && poetry --version \
    && poetry config virtualenvs.in-project true

SHELL ["/bin/bash", "-c"]

FROM base as prod

RUN useradd --create-home --shell /bin/bash pdf-link-checker-user

ENV PATH="$PATH:/home/pdf-link-checker-user/.local/bin"
WORKDIR /home/pdf-link-checker-user
USER pdf-link-checker-user

COPY --chown=pdf-link-checker-user dist dist

# Install the python package
RUN pip install -q --no-cache-dir ./dist/*whl \
    && rm -rf ./dist/ \
    && pdf-link-checker --install-completion bash

# Harden the image
USER root

RUN chmod u-s,g-s /usr/bin/* \
    && chmod u-s,g-s /bin/* \
    && chmod u-s,g-s /sbin/*

USER pdf-link-checker-user

HEALTHCHECK --interval=5m --timeout=3s CMD [ "pdf-link-checker", "--version" ]
