# peterborough-open-gov

## Setup

Install [`pipenv`](https://pypi.org/project/pipenv/). On MacOS:
```sh
brew install pipenv
```


```sh
# cd into project folder
pipenv --three       # create a new virtualenv
pipenv shell         # activate virtualenv
```

Install dependencies like this:
```sh
pipenv install       # install only default packages
```

Or if you need the dev dependencies, install like this:
```sh
pipenv install --dev # install dev packages and default
```

Start the jupyter notebook server: `jupyter lab`

To start the webserver:
```sh
./start.sh
```