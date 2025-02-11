FROM mcr.microsoft.com/devcontainers/python:3.9

# runtime dependencies
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		awscli

WORKDIR /workspaces/peterborough-open-gov

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG CITY_COUNCIL_SCRAPER_S3_BUCKET
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}
ENV CITY_COUNCIL_SCRAPER_S3_BUCKET ${CITY_COUNCIL_SCRAPER_S3_BUCKET}

# Upgrade pip and install requirements
RUN pip install --upgrade pip

ENTRYPOINT ["/workspaces/peterborough-open-gov/.devcontainer/install.sh"]