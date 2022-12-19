# To run scraper

`npx playwright test tests/city-council.spec.ts --headed`

## To build docker container

```sh
docker build -t city-council-scraper .
```

### To push a new image to amazon ECR

`aws configure`
login to AWS console, go to AWS ECR, follow the "push commands" steps

## To run the playwright scraper

```sh
docker run city-council-scraper
```