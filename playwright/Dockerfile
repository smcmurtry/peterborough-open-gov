FROM mcr.microsoft.com/playwright:v1.28.0-focal

# copy project (including tests)
COPY . /playwright

WORKDIR /playwright

# Install dependencies
RUN npm install

# Install browsers
RUN npx playwright install

# Run playwright test
CMD [ "npx", "playwright", "test", "tests/city-council.spec.ts" ]