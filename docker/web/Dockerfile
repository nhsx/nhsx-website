FROM alpine:3.14 as base

ENV VERSION 1.9.1

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN apk update && apk add --no-cache \
    python3-dev \
    automake \
    bash \
    bzip2-dev \
    cairo \
    ca-certificates \
    cmake \
    curl \
    freetype-dev \
    ncurses-dev \
    gcc \
    g++ \
    git \
    glib \
    jpeg-dev \
    libc-dev \
    libffi-dev \
    libpng-dev \
    libsass \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    make \
    nano \
    openssh \
    pango \
    postgresql-dev \
    readline-dev \
    sqlite-dev \
    sqlite \
    zlib-dev \
    nodejs \
    npm \
    zsh && \
    rm -f /tmp/* /etc/apk/cache/* /root/.cache

####################################################################################################
# Install static asset compilers
####################################################################################################

# work around a bug in the version of node we are using
# https://github.com/npm/uid-number/issues/3
# https://github.com/nodejs/docker-node/issues/813
RUN npm config set unsafe-perm true

# Install babel?
RUN npm install --no-cache --global babel-cli \
    babel-preset-env \
    uglify-js \
    wait-for && \
    rm -f /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/configstore/node_modules/dot-prop/license
RUN npm config set unsafe-perm false

# Install libsass
RUN pip install --no-cache-dir \
    libsass \
    closure

FROM base AS app

# Install envkey-source
RUN curl -s https://raw.githubusercontent.com/envkey/envkey-source/master/install.sh | bash

# Install and set up Poetry for python dependencies management
ENV POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_PATH="/usr/venvs" \
    POETRY_REPOSITORIES={} \
    POETRY_VERSION=1.2.2

# Attempting to fix issues with broken pip installs -- something like:
# ImportError: cannot import name 'InvalidSchemeCombination' from 'pip._internal.exceptions'
# https://askubuntu.com/questions/1025189/pip-is-not-working-importerror-no-module-named-pip-internal

# Linking of pip/python and deleting of directories from original pip install: not known if needed.

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --force-reinstall && \
    rm /usr/bin/pip && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    rm /usr/bin/python && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /tmp/* /etc/apk/cache/* /root/.cache

RUN curl -sSL https://install.python-poetry.org | python

RUN mkdir -p /usr/srv/app/
WORKDIR /usr/srv/app/

# Ensure docker-compose build web is able to pass these env vars in
ARG SERVER_ENV

ENV DOCKERFILE_VERSION=1.1

####################################################################################################
# PROJECT STUFF
####################################################################################################

# Not really sure what this is for. Best leave it alone.
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/srv/app/

# npm install
COPY ./package.json package.json
COPY ./package-lock.json package-lock.json
RUN npm install
RUN mkdir -p /usr/srv/deps
RUN mv ./node_modules/ /usr/srv/deps

# POETRY (working and installed in django-base)
COPY ./app/pyproject.toml /usr/srv/app/pyproject.toml
COPY ./app/poetry.lock /usr/srv/app/poetry.lock
## self update disabled currently due to causing timeout issues in the deploy
#RUN $HOME/.local/bin/poetry self update 1.2.2 && \
RUN $HOME/.local/bin/poetry install


VOLUME /usr/srv/app/media


RUN apk update && \
    apk add --no-cache rsync libsass-dev

# Expose the dev server
EXPOSE 5000

FROM app as dev

####################################################################################################
# Install fish quickly from apk
####################################################################################################

RUN apk update && \
    apk add --no-cache fish && \
    rm -rf /tmp/* /etc/apk/cache/*

ENV SHELL /bin/zsh

# Add fish config
RUN mkdir -p ~/.config/fish
COPY ./docker/web/conf/config.fish /tmp/config.fish
RUN mv /tmp/config.fish ~/.config/fish/config.fish

WORKDIR /usr/srv/app/

# We'll eventually want these or similar for the production container
# RUN python manage.py migrate

# COPY ./docker/web/conf/uwsgi.ini /etc/uwsgi.ini

# RUN addgroup -S wagtail
# RUN adduser -S -D -h /usr/srv/app wagtail wagtail
# RUN chown -R wagtail /usr/srv/app/
# USER wagtail

# EXPOSE 8000
# CMD exec uwsgi --static-map /static=/src/app/static --ini /etc/uwsgi.ini
