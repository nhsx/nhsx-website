FROM alpine:3.7 as base

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
    mdocml-apropos \
    nano \
    openssh \
    pango \
    postgresql-dev \
    py-pysqlite \
    readline-dev \
    sqlite-dev \
    sqlite \
    zlib-dev \
    nodejs \
    nodejs-npm \
    zsh && \
    rm -f /tmp/* /etc/apk/cache/* /root/.cache

####################################################################################################
# Install static asset compilers
####################################################################################################

RUN apk add closure-compiler --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted && \
    rm -f /tmp/* /etc/apk/cache/* /root/.cache

# Install babel?
RUN npm install --no-cache --global babel-cli \
    babel-preset-es2015 \
    uglify-js \
    wait-for && \
    rm -f /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/configstore/node_modules/dot-prop/license

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
    POETRY_REPOSITORIES={}

RUN apk add --no-cache --update py3-pip && \
    rm /usr/bin/pip && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    rm /usr/bin/python && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -f /tmp/* /etc/apk/cache/* /root/.cache

RUN set -ex pip install --no-cache-dir pip --upgrade && \
    rm -f /tmp/* /etc/apk/cache/* /root/.cache && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    source $HOME/.poetry/env

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

# POETRY (working and installed in django-base)
WORKDIR /usr/srv/app/
COPY ./app/pyproject.toml /usr/srv/app/pyproject.toml
COPY ./app/poetry.lock /usr/srv/app/poetry.lock
RUN source $HOME/.poetry/env && \
    poetry self update && \
    poetry install


RUN whoami
RUN ls -la


VOLUME /usr/srv/app/media


RUN apk update && \
    apk add --no-cache rsync libsass-dev

# Expose the dev server
EXPOSE 5000

FROM app as dev

####################################################################################################
# Install latest Fish shell from source
####################################################################################################

WORKDIR /tmp
RUN wget https://github.com/fish-shell/fish-shell/releases/download/3.1.0/fish-3.1.0.tar.gz && \
    tar -xvzf fish-3.1.0.tar.gz && \
    cd fish-3.1.0 && \
    cmake . && \
    make && \
    make install && \
    rm -rf /tmp/*

ENV SHELL /bin/zsh

# Install oh-my-zsh and set zsh as the default shell
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

COPY ./docker/web/conf/zshrc /tmp/.zshrc
COPY ./docker/web/conf/hactar.zsh-theme /tmp/hactar.zsh-theme
COPY ./docker/web/conf/zsh-auto-suggest.cfg /tmp/config.zsh

RUN mv /tmp/.zshrc ~/.zshrc && \
    mv /tmp/hactar.zsh-theme ~/.oh-my-zsh/themes/hactar.zsh-theme && \
    mv /tmp/config.zsh ~/.oh-my-zsh/custom/config.zsh && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    rm -rf /tmp/*

CMD ["zsh", "--version"]

# Add fish config
RUN mkdir -p ~/.config/fish
COPY ./docker/web/conf/config.fish /tmp/config.fish
RUN mv /tmp/config.fish ~/.config/fish/config.fish

WORKDIR /usr/srv/app/

# We'll eventually want these or similar for the production container
# RUN python manage.py migrate

# RUN useradd wagtail
# RUN chown -R wagtail /code
# USER wagtail

# EXPOSE 8000
# CMD exec gunicorn nhsx.wsgi:application --bind 0.0.0.0:8000 --workers 3
