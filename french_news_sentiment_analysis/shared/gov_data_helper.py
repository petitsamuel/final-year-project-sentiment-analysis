from .models import GouvSyntheseModel
from datetime import datetime

# Useful methods when using data provided by the French Government


def grab_metric_from_data(data, metric):
    selected_metric = []
    for d in data:
        if metric in d:
            parsed_date = datetime.strptime(
                d[GouvSyntheseModel.date], '%Y-%m-%d')
            selected_metric.append([parsed_date, d[metric]])
    return sorted(selected_metric, key=lambda x: x[0])


# Most of the data provided by the FR gov is cumulative
# This method makes the data non-cumulative
def de_sum_data(data):
    for i in reversed(range(1, len(data))):
        data[i] = max(0, data[i] - data[i - 1])
    return data
