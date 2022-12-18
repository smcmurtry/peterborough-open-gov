FROM python:3.9-alpine3.13

RUN apk add --no-cache \
    autoconf \
    automake \
    bash \
    build-base \
    cmake \
    g++ \
    git \
    libexecinfo-dev \
    libffi-dev \
    libtool \
    libxml2-dev \
    libxslt-dev \    
    nodejs \
    npm \    
    nodejs \ 
    make     

# Upgrade pip
RUN pip install --upgrade pip

COPY ci/scripts/entrypoint.sh /usr/local/bin/

EXPOSE 5000
