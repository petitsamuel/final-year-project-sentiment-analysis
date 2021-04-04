from shared.file_read_write import read_file
import matplotlib.pyplot as plt
from shared.models import GouvSyntheseModel
import json
from datetime import datetime


# Most of the data provided by the FR gov is cumulative
# This method makes the data non-cumulative
def de_sum_data(data):
    for i in reversed(range(1, len(data))):
        data[i] = max(0, data[i] - data[i - 1])
    return data


def grab_metric_from_data(data, metric):
    selected_metric = []
    for d in data:
        if metric in d:
            parsed_date = datetime.strptime(
                d[GouvSyntheseModel.date], '%Y-%m-%d')
            selected_metric.append([parsed_date, d[metric]])
    return sorted(selected_metric, key=lambda x: x[0])


def plot_vaccination():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(
        data, GouvSyntheseModel.cumulPremieresInjections)

    dates, values = zip(*metrics)
    values = de_sum_data(list(values))

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='First Vaccination Shot')
    ax.set_xlabel("Date")
    ax.set_title("COVID-19 First Vaccine Injections in France")
    ax.legend(loc='upper left')


def plot_cases_fr():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.casConfirmes)

    dates, values = zip(*metrics)
    values = de_sum_data(list(values))

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, values, label='New cases')
    ax.set_title("COVID-19 Cases in France")
    ax.legend(loc='upper left')


def plot_deaths_fr():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.deces)

    dates, values = zip(*metrics)
    values = de_sum_data(list(values))

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values)
    ax.set_ylabel("Number of Deaths")
    ax.set_title("COVID-19 Deaths in France")


def plot_hospitalise():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.hospitalises)

    dates, values = zip(*metrics)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values)
    ax.set_ylabel("Number of Hospitalised Patients")
    ax.set_title("COVID-19 Hospitalised Patients in France")


def tests_quantite():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.testsRealises)

    dates, values = zip(*metrics)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='Tests')
    ax.set_title("Number of COVID-19 Tests in France")
    ax.legend(loc='upper left')


tests_quantite()
plot_cases_fr()
plot_deaths_fr()
plot_vaccination()
plot_hospitalise()
plt.show()
