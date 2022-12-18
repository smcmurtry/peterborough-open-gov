# using a debian-based image because the alpine images takes 
# forever to build pandas
FROM python:3.9-slim-buster

WORKDIR /peterborough-open-gov
COPY . /peterborough-open-gov

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

COPY entrypoint.sh /peterborough-open-gov/ci/entrypoint.sh

ENTRYPOINT ["/peterborough-open-gov/ci/entrypoint.sh"]