from shared.file_read_write import read_file
import matplotlib.pyplot as plt
from shared.models import GouvSyntheseModel
import json
from datetime import datetime


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

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='First Vaccination Shot')
    ax.set_xlabel("Date")
    ax.set_title("COVID19 First Vaccin Injections in France")
    ax.legend(loc='lower right')


def plot_cases_fr():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.casConfirmes)

    dates, values = zip(*metrics)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='Cases Count')
    ax.set_xlabel("Date")
    ax.set_title("COVID19 Cases in France")
    ax.legend(loc='lower right')


def plot_deaths_fr():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.deces)

    dates, values = zip(*metrics)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='Deaths')
    ax.set_xlabel("Date")
    ax.set_title("COVID19 Related Deaths in France")
    ax.legend(loc='lower right')


def plot_hospitalise():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.hospitalises)

    dates, values = zip(*metrics)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='Hospitalised')
    ax.set_xlabel("Date")
    ax.set_title("COVID19 Hospitalised Patients in France")
    ax.legend(loc='lower right')


def tests_quantite():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    metrics = grab_metric_from_data(data, GouvSyntheseModel.testsRealises)

    dates, values = zip(*metrics)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(dates, values, label='testsRealises')
    ax.set_xlabel("Date")
    ax.set_title("COVID19 testsRealises in France")
    ax.legend(loc='lower right')


tests_quantite()
plot_cases_fr()
plot_deaths_fr()
plot_vaccination()
plot_hospitalise()
plt.show()
