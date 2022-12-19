# peterborough-open-gov

## Setup

Open project in VS code as a dev container.

Start the jupyter notebook server: `jupyter lab`

To start the webserver:
```sh
./start.sh
```

## Scraping

To run playwright

```
cd playwright
npx playwright test tests/city-council.spec.ts --headed
```

To parse the scraped data and download the pdfs, start the dev container and then run:
```
cd python-etl-scraper
```

