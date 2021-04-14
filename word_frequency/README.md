# Word Frequency

This small project enables computing word frequencies for the set of `*.txt` documents within the `texts/` directory.

The script will compute the relative frequency for words within all of the text documents, it uses word lemmatization from the spacy open source package. It can also output file specific word frequencies.

It is setup for French texts however you may change the spacy package used from `fr_core_news_sm` to any other language from [SpaCy](https://spacy.io/usage/models). Make sure to install it with the command below and change the package used in `./file_reader.py`.

This project did not get pushed much further.

## Setup

Run the following commands to download required packages:

`pip instal -r dependencies.txt`

`python -m spacy download fr_core_news_sm`

## Running

`python script.py`

The script will output the set of relative frequencies as a CSV file in the `./outputs` directory.
