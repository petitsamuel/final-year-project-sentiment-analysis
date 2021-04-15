from shared.db_helpers import init_db, fetch_script_from_db
from shared.dates_helper import to_datetime
from shared.file_read_write import read_file
from shared.models import GouvSyntheseModel
from shared.gov_data_helper import grab_metric_from_data, de_sum_data
from shared.folders import deaths_sentiment_csv, virus_sentiment_csv, vaccine_sentiment_csv
from shared.file_read_write import write_dict_array_to_csv
import json
import csv


# Grab article counts daily from the DB along with the data. Merge the data with
# data from the French Goverment: daily covid-19 deaths.
# This generates a csv file in the data directory & will be used to compute correlations.


def default_vaccine_dict_entry(date):
    return {
        'date': date,
        'article_count': 0,
        'injections_count': 0,
        'injections_cumulated': 0,
        'dict_hits': 0,
        'average_hits_per_article': 0,
        'average_hits_per_words': 0
    }


def default_death_dict_entry(date):
    return {
        'date': date,
        'article_count': 0,
        'death_count': 0,
        'deaths_cumulated': 0,
        'dict_hits': 0,
        'average_hits_per_article': 0,
        'average_hits_per_words': 0
    }


def default_virus_dict_entry(date):
    return {
        'date': date,
        'article_count': 0,
        'cases_count': 0,
        'cases_cumulated': 0,
        'dict_hits': 0,
        'average_hits_per_article': 0,
        'average_hits_per_words': 0
    }


def format_dates(data):
    for d in data:
        d['date'] = d['date'].strftime(r"%d/%m/%Y")
    return data


def add_article_counts_to_data(default_dict):
    data = {}
    for count, day, month, year in counts:
        date = to_datetime(day, month, year)
        data[date] = default_dict(date)
        data[date]['article_count'] = count
    return data


def add_sentiment_to_data(data, sentiment_script):
    sentiment = fetch_script_from_db(sentiment_script)
    for _, dict_hits, avg_hits_per_article, avg_hits_per_word, day, month, year in sentiment:
        date = to_datetime(day, month, year)
        data[date]['dict_hits'] = dict_hits
        data[date]['average_hits_per_article'] = avg_hits_per_article
        data[date]['average_hits_per_words'] = avg_hits_per_word

    return data


def get_gov_metric(metric, decumul=True):
    assert(gouv_data)
    # Extract dates and specified metric
    gouv_metrics = grab_metric_from_data(gouv_data, metric)
    dates, cumulated = zip(*gouv_metrics)

    if not decumul:
        return dates, cumulated

    uncumulated = de_sum_data(list(cumulated))
    return dates, uncumulated, cumulated


def prepare_data_for_csv(data):
    data = sorted(data.values(), key=lambda item: item['date'])
    data = format_dates(data)
    return data


def merge_death_into_csv():
    assert(gouv_data)
    assert(counts)

    data = add_article_counts_to_data(default_death_dict_entry)
    data = add_sentiment_to_data(data, 'sentiment_death_daily.sql')

    # Get Gov Data
    gouv_dates, gouv_deaths, cumul_gouv_deaths = get_gov_metric(
        GouvSyntheseModel.deces)

    for i in range(len(gouv_deaths)):
        date = gouv_dates[i]
        deaths = gouv_deaths[i]
        cumul = cumul_gouv_deaths[i]
        if date not in data:
            data[date] = default_death_dict_entry(date)

        data[date]['death_count'] = deaths
        data[date]['deaths_cumulated'] = cumul

    data = prepare_data_for_csv(data)

    # Write to CSV
    write_dict_array_to_csv(data, deaths_sentiment_csv)
    print("Saved data to CSV into %s" % (deaths_sentiment_csv))


def merge_virus_into_csv():
    assert(gouv_data)
    assert(counts)

    data = add_article_counts_to_data(default_virus_dict_entry)
    data = add_sentiment_to_data(data, 'sentiment_virus_daily.sql')

    # Get Gov Data
    gouv_dates, gouv_cases, cumul_gouv_cases = get_gov_metric(
        GouvSyntheseModel.casConfirmes)

    for i in range(len(gouv_cases)):
        date = gouv_dates[i]
        cases = gouv_cases[i]
        cumul = cumul_gouv_cases[i]
        if date not in data:
            data[date] = default_virus_dict_entry(date)

        data[date]['cases_count'] = cases
        data[date]['cases_cumulated'] = cumul

    data = prepare_data_for_csv(data)

    # Write to CSV
    write_dict_array_to_csv(data, virus_sentiment_csv)
    print("Saved data to CSV into %s" % (virus_sentiment_csv))


def merge_vaccine_into_csv():
    assert(gouv_data)
    assert(counts)

    data = add_article_counts_to_data(default_vaccine_dict_entry)
    data = add_sentiment_to_data(data, 'sentiment_vaccine_daily.sql')

    # Get Gov Data
    gouv_dates, gouv_injections = get_gov_metric(
        GouvSyntheseModel.nouvellesPremieresInjections, False)
    _, cumul_gouv_injections = get_gov_metric(
        GouvSyntheseModel.cumulPremieresInjections, False)

    for i in range(len(gouv_injections)):
        date = gouv_dates[i]
        injections = gouv_injections[i]
        cumul_injections = cumul_gouv_injections[i]
        if date not in data:
            data[date] = default_vaccine_dict_entry(date)

        data[date]['injections_count'] = injections
        data[date]['injections_cumulated'] = cumul_injections

    data = prepare_data_for_csv(data)

    # Write to CSV
    write_dict_array_to_csv(data, vaccine_sentiment_csv)
    print("Saved data to CSV into %s" % (vaccine_sentiment_csv))


init_db()

# Load article counts
counts = fetch_script_from_db("count_daily.sql")

# Load government dataset
gouv_data = json.loads(read_file('gouv/synthese-fra.json'))

merge_death_into_csv()
merge_virus_into_csv()
merge_vaccine_into_csv()
