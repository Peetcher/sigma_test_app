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

    if delta <= datetime.timedelta(days=30):
        step = datetime.timedelta(days=1)
    elif datetime.timedelta(days=30) < delta < datetime.timedelta(days=365):
        step = datetime.timedelta(weeks=1)
    elif delta > datetime.timedelta(365):
        step = datetime.timedelta(weeks=2)
    else:
        raise Exception("некорректный промежуток времени")

    return step


# рассчёт точки
def calc_point(dataset, start_index, target, index):
    price_array = numpy.array([item[target] for item in dataset[start_index: index]])

    bottom_bound = int(price_array.mean() - price_array.std())
    upper_bound = int(price_array.mean() + price_array.std())

    price_array = price_array.tolist()
    price_array = [num for num in price_array if num in range(bottom_bound - 1, upper_bound + 1)]
    point = int(mean(price_array))
    return point


def append_point(result, step, point, start_date):
    if step == datetime.timedelta(weeks=1) and result:
        date = parser.parse(result[-1]["date"]) + step
        result.append({"date": date.isoformat(), "price": point})
    else:
        result.append({"date": start_date.isoformat(), "price": point})


# удаление выбросов
def remove_outliers(dataset, step, target):
    start_date = parser.parse(dataset[0]["date"])
    start_index = 0

    result = []

    for index, node in enumerate(dataset):
        node_date = parser.parse(node["date"])
        if start_date + step <= node_date < start_date + (step * 2):
            point = calc_point(dataset, start_index, target, index)
            result.append({"date": start_date.isoformat(), "price": point})

            start_index = index
            start_date += step
        else:
            if node_date >= start_date + (step * 2):
                if index != 0:  # если точка не первая
                    point = calc_point(dataset, start_index, target, index)
                    result.append({"date": start_date.isoformat(), "price": point})
                    start_date += step

                    delta = int((node_date - start_date) / step)
                    for day in range(1, delta):  # заполняем недостающую разницу точками с price = предыдущее значение
                        result.append({"date": start_date.isoformat(), "price": result[-1]["price"]})
                        start_date += step

                else:  # если точка первая, то точка = 0
                    result.append({"date": start_date, "price": 0})
                    start_date += step
                start_index = index
            continue

    return result


# очистка данных и возврат output
def facade(json_data: dict):
    target = json_data["target"]
    dataset = json_data["data"]

    date_from = parser.parse(json_data["dateFrom"])
    date_to = parser.parse(json_data["dateTo"])
    delta = date_to - date_from

    dataset = select_range(dataset, date_from, date_to)
    step = define_step(delta)

    result = remove_outliers(dataset, step, target)
    print(result)

    return result



