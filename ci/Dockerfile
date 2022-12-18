FROM python:3.9-alpine3.13@sha256:a7cbd1e7784a35a098cedbc8681b790d35ff6030a5e13f043185e2465003a040

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils 2>&1 \
    && apt-get -y install \
    curl \
    emacs \
    exa \
    fd-find \
    git \ 
    iproute2 \
    less \ 
    libsodium-dev \
    lsb-release \ 
    man-db \
    manpages \
    net-tools \
    nodejs \ 
    npm \
    openssh-client \ 
    procps \ 
    tldr \
    unzip \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

COPY ci/scripts/entrypoint.sh /usr/local/bin/

EXPOSE 5000
