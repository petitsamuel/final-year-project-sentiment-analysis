from shared.file_read_write import read_file
import matplotlib.pyplot as plt
from shared.models import GouvSyntheseModel
from shared.gov_data_helper import grab_metric_from_data, de_sum_data
import json
from datetime import datetime


# Plots data provided by the French government on Covid cases, deaths vaccinations...


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
    ax.bar(dates, values, label='New cases')
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
