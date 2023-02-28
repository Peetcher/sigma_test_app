import numpy
import datetime
import json
from dateutil import parser
from statistics import mean


# выбираем диапазон заданный в json
def select_range(dataset, date_from, date_to):
    start_index = None
    stop_index = None

    for index, node in enumerate(dataset):
        date = parser.parse(node["date"])

        if start_index is None:
            if date >= date_from:
                start_index = index

        if stop_index is None:
            if date >= date_to:
                stop_index = index

    dataset = dataset[start_index:stop_index]

    return dataset


# определение шага
def define_step(delta):
    step = None

    if delta <= datetime.timedelta(days=60):
        step = datetime.timedelta(days=1)
    elif datetime.timedelta(days=60) < delta < datetime.timedelta(days=365):
        step = datetime.timedelta(weeks=1)
    elif delta > datetime.timedelta(365):
        step = datetime.timedelta(weeks=2)
    else:
        raise Exception("некорректный промежуток времени")

    return step


# удаление выбросов
def remove_outliers(dataset, step, target):
    start_date = parser.parse(dataset[0]["date"])
    start_index = 0

    result = []

    for index, node in enumerate(dataset):
        node_date = parser.parse(node["date"])
        if node_date >= start_date + step:
            price_array = numpy.array([item[target] for item in dataset[start_index: index]])

            bottom_bound = int(price_array.mean() - price_array.std())
            upper_bound = int(price_array.mean() + price_array.std())

            price_array = price_array.tolist()
            price_array = [num for num in price_array if num in range(bottom_bound - 1, upper_bound + 1)]

            result.append({"date": start_date.isoformat(), "price": int(mean(price_array))})

            start_index = index
            start_date = parser.parse(node["date"])
    return result


# очистка данных и возврат output
def sigma_clean(json_data: dict):
    target = json_data["target"]
    dataset = json_data["data"]

    date_from = parser.parse(json_data["dateFrom"])
    date_to = parser.parse(json_data["dateTo"])
    delta = date_to - date_from

    dataset = select_range(dataset, date_from, date_to)
    step = define_step(delta)

    result = remove_outliers(dataset, step, target)

    return result
