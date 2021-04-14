from shared.db_helpers import init_db, fetch_script_from_db
from shared.dates_helper import to_datetime
from shared.file_read_write import read_file
from shared.models import GouvSyntheseModel
from shared.gov_data_helper import grab_metric_from_data, de_sum_data
from shared.folders import deaths_sentiment_csv
from shared.file_read_write import write_raw_to_file
import json


# Grab article counts daily from the DB along with the data. Merge the data with
# data from the French Goverment: daily covid-19 deaths.
# This generates a csv file in the data directory & will be used to compute correlations.


def merge_into_csv():
    # Load article counts
    init_db()
    counts = fetch_script_from_db("count_daily.sql")
    data = {}
    for count, day, month, year in counts:
        date = to_datetime(day, month, year)
        data[date] = {'article_count': count, 'date': date,
                      'death_count': 0, 'deaths_cumulated': 0}

    # Load government dataset
    gouv_data = json.loads(read_file('gouv/synthese-fra.json'))
    # Extract dates and death rates
    gouv_metrics = grab_metric_from_data(gouv_data, GouvSyntheseModel.deces)
    gouv_dates, cumul_gouv_deaths = zip(*gouv_metrics)
    gouv_deaths = de_sum_data(list(cumul_gouv_deaths))

    for i in range(len(gouv_deaths)):
        date = gouv_dates[i]
        deaths = gouv_deaths[i]
        cumul = cumul_gouv_deaths[i]
        if date not in data:
            data[date] = {'death_count': deaths, 'deaths_cumulated': cumul,
                          'date': date, 'article_count': 0}
            continue
        data[date]['death_count'] = deaths
        data[date]['deaths_cumulated'] = cumul

    # Sort
    data = sorted(data.values(), key=lambda item: item['date'])
    # Format dates
    for d in data:
        d['date'] = d['date'].strftime(r"%d/%m/%Y")

    csv_out = 'date,deaths,articles,deaths_cumulated'
    for d in data:
        csv_out += '\n%s,%d,%d,%d' % (d['date'],
                                      d['death_count'], d['article_count'], d['deaths_cumulated'])
    write_raw_to_file(csv_out, deaths_sentiment_csv)
    print("Saved data to CSV into %s" % (deaths_sentiment_csv))


merge_into_csv()
