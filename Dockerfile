FROM python:3.9-bullseye

ARG COMMIT=""
ARG COMMIT_SHORT=""
ARG BRANCH=""
ARG TAG=""

LABEL author="Patrick Stöckle <patrick.stoeckle@tum.de>"
LABEL edu.tum.i4.pdf-link-checker.commit=${COMMIT}
LABEL edu.tum.i4.pdf-link-checker.commit-short=${COMMIT_SHORT}
LABEL edu.tum.i4.pdf-link-checker.branch=${BRANCH}
LABEL edu.tum.i4.pdf-link-checker.tag=${TAG}

ENV COMMIT=${COMMIT}
ENV COMMIT_SHORT=${COMMIT_SHORT}
ENV BRANCH=${BRANCH}
ENV TAG=${TAG}

COPY sources.list /etc/apt/sources.list

RUN apt-get update -qq \
    && apt-get autoremove -y -qq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash pdf-link-checker-user
WORKDIR /home/pdf-link-checker-user

COPY dist dist

RUN chown pdf-link-checker-user dist

USER pdf-link-checker-user

RUN pip install --no-cache-dir --upgrade pip==21.3.1 \
    && pip install --no-cache-dir dist/*.whl \
    && rm -rf dist

ENV PATH="${PATH}:/home/pdf-link-checker-user/.local/bin"

RUN pdf-link-checker --version
