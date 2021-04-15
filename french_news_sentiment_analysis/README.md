# French News Sentiment Analysis

## Dependencies

`pip install -r dependencies.txt`

`python -m spacy download fr_core_news_lg`

Make sure to install PyTorch:

[PyTorch](https://pytorch.org/get-started/locally/)

## LexisNexis Scraper

TODO: Dockerize this system.

A scraper to download articles from Lexis Nexis automatically. Note that the scraper has been written for Trinity College Dublin's login system for LexisNexis, if you are not a TCD student you may want to update the
following 2 methods from `./ln_scraper.py`:

```python
def login_user(url):

def check_tcd_limit_reached():
```

### How to use

Note that the following setup is only required for the scrapper, if you are not looking to use the scrapper you may skip these steps.

Download the chromedriver [here](https://chromedriver.chromium.org/downloads)

Make sure to make it executable

`chmod +x chromedriver`

And that you have google-chrome in your path

`google-chrome --version`

### .env file

Create a .env file in this directory with the following parameters:

```.env
PAGE_SIZE=500
TIMEOUT=300
CHROME_DRIVER="<PATH_TO_CHROME_DRIVER_FILE>"
LN_PASSWORD="<YOUR_TCD_PASSWORD>"
LN_USERNAME="<YOUR_TCD_USERNAME>"
```

### Running

Before running the script you will want to generate a set of URLs which match the filters you are looking to download articles from. Then click "generate parmanent link" from the set of actions on the LexisNexis Website.

Once you have the link, make the following changes to `./ln_scraper.py`:

- Add the link to the URLS array

- Add the amount of articles that match your filters (go to the last page) to the COUNTS array. Note that LexisNexis will break when using an offset of over 30 000, so make sure to use the date filtering such as to create batches of articles to download.

- Add the batch identifier the the BATCH_ID array

You're now ready to start downloading! Run:
`./scripts/scrape.sh`

## Loading the Data & DB

### Setup

The database for this project is MySQL and runs within a docker container. Install:

- [docker](https://docs.docker.com/get-docker/)

- [docker-compose](https://docs.docker.com/compose/install/)

Then add the following variables to the `./.env` file (in this directory):

```.env
MYSQL_ROOT_PASSWORD=root
MYSQL_USER=admin
MYSQL_PASSWORD=password
MYSQL_DATABASE=fr_covid_news
MYSQL_HOST=127.0.0.1
```

### Running the DB

To run the DB:

```bash
docker-compose up -d # use -d to run in detached mode
```

To kill the DB:

```bash
docker-compose down # use -v to clear the DB's data
```

To run the DB and wait for the container to be healthy (initialisation finished & ready for requests):

```bash
./scripts/run_db.sh
```

### Loading Data into DB

To load data downloaded from the LexisNexis Scrapper run:

`python load_data_into_db.py`

You can also run this script in parallel with the scrapper:

`./scripts/db_loader.sh`

This will run the script, import available data, then sleep 40 minutes and check for new data.

### Useful Commands

Logging into DB using mysql CLI tool:

`mysql --host=127.0.0.1 --port=3306 -uadmin -ppassword`

Logging into DB using docker container:

`docker exec -it fr_news_db mysql -uadmin -ppassword`

Dumping data to a file:

`mysqldump -h 127.0.0.1 -u root -p fr_covid_news > dump_treetagger.sql`

## TODO

- data analysis & plots

- sentiment analysis systems
