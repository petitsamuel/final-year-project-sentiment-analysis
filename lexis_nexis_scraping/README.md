# LexisNexis

## Dependencies

`pip install -r dependencies.txt`

`python -m spacy download fr_core_news_sm`

## Requirement

LexisNexis Uni subscription

python v3.6

pandas v0.20.1

selenium v3.141

chromedriver.exe

### .env

Create a .env file in this directory with the following parameters:

```
MYSQL_ROOT_PASSWORD=root
MYSQL_USER=admin
MYSQL_PASSWORD=password
MYSQL_DATABASE=fr_covid_news
MYSQL_HOST=127.0.0.1
PAGE_SIZE=500
TIMEOUT=300
```
