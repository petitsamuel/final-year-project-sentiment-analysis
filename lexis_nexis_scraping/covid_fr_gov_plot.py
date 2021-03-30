from shared.variable_loader import read_file
import matplotlib.pyplot as plt
import json
import datetime


def plot_cases_fr():
    data = json.loads(read_file('gouv/synthese-fra.json'))
    print(data)
    # Sort data by week number
    # data = dict(sorted(data.items(), key=lambda item: int(item[0])))

    # # Grab list of week numbers and format data in form word -> [count, count...]
    # dates = data.keys()
    # output_dict = format_weekly_data(data)

    # # plot data
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # for key, value in output_dict.items():
    #     ax.plot(dates, value, label=key)
    # ax.set_xlabel("Week")
    # ax.set_title("Most frequent word count in %s per week" % (data_source))
    # ax.legend(loc='lower right')


plot_cases_fr()
# plt.show()
