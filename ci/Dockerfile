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

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG CITY_COUNCIL_SCRAPER_S3_BUCKET
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}
ENV CITY_COUNCIL_SCRAPER_S3_BUCKET ${CITY_COUNCIL_SCRAPER_S3_BUCKET}

# Upgrade pip
RUN pip install --upgrade pip

COPY ci/scripts/entrypoint.sh /usr/local/bin/

EXPOSE 5000
