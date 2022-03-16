# URPARTS Scraper

Urparts web scraper is a simple FastAPI, SQLModel, Python application that scraps machine parts data from https://www.urparts.com/index.cfm/page/catalogue/,
saves the data to a database and exposes an endpoint `http://127.0.0.1:8000/api/parts?limit=5` see swagger docs on `http://127.0.0.1:8000/docs` when the app is running.

- A user can query for parts using parameters; see swagger docs

#### Technologies

- Python 3.9
- FastAPI
- SQLModel
- httpx

## Setup

clone repo and cd into the directory

make sure you have docker running on your system

run: `docker compose up` from the root directory of the project

It will create a database, start a web scraper that will populate the database, and start a web application on port 8000

Note:

- Once the server is started, it takes a few milliseconds to start seeing data
- It takes about 2 minutes to scrape all the data, after which you will see `web_scraper_1 exited with code 0` on the docker terminal
- Once you see `web_scraper_1 exited with code 0` no more services are running, and all the data is in the DB

- Stop service running on port 8000 and run `docker compose up` again if the port is busy

#### AUTHOR

Godswill
