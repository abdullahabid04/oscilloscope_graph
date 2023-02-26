import numpy as np
import re
from matplotlib.dates import date2num, num2date
from datetime import datetime
import itertools
from collections import OrderedDict
from requirements import config


def convert_time_format(t):
    datetime_re = re.compile(r'[\d]{2,6}')

    num_to_date = num2date(t)
    date_to_regex = datetime_re.findall(str(num_to_date))
    date_time_object = datetime(*list(map(int, date_to_regex[:-2])))

    return (num_to_date, date_to_regex, date_time_object)


def find_next_idx(indexes, last):
    for index in indexes:
        if index > last:
            return index + 1

    return 100000


def remove_adjacents(duty_cycles):
    return [k for k, v in itertools.groupby(duty_cycles)]
    # return [k for k, g in itertools.groupby(duty_cycles)]


def drop_duplicates(cycles):
    return list(OrderedDict.fromkeys(cycles))


def format_wave(wave):
    wave_mean = np.mean(wave)
    high, low = get_high_low_values(wave, wave_mean)

    for index, item in enumerate(wave):
        if item > wave_mean:
            wave[index] = high
        if item < wave_mean:
            wave[index] = low

    wave = np.array(wave)

    return wave


def get_high_low_values(wave_form, mean_value):
    high_values, low_values = [], []

    for item in wave_form:
        if item > mean_value:
            high_values.append(item)
        if item < mean_value:
            low_values.append(item)

    high_avg, low_avg = np.average(high_values), np.average(low_values)

    return round(high_avg, 5), round(low_avg, 5)


def max_k_values(x, k=25):
    a = dict([(i, j) for i, j in enumerate(x)])
    sorted_a = dict(sorted(a.items(), key=lambda kv: kv[1], reverse=True))
    indices = list(sorted_a.keys())[:k]
    values = list(sorted_a.values())[:k]
    return (indices, values)


def min_k_values(x, k=25):
    a = dict([(i, j) for i, j in enumerate(x)])
    sorted_a = dict(sorted(a.items(), key=lambda kv: kv[1], reverse=True))
    indices = list(sorted_a.keys())[len(sorted_a) - k:]
    values = list(sorted_a.values())[len(sorted_a) - k:]
    return (indices, values)


def remove_duplicates(df):
    columns_to_drop = []

    for cname in sorted(list(df)):
        for cname2 in sorted(list(df))[::-1]:
            if df[cname].equals(df[cname2]) and cname != cname2 and cname not in columns_to_drop:
                columns_to_drop.append(cname2)

    df = df.drop(columns_to_drop, axis=1)

    return df


def calculate_moving_averages(data, threshold=3):
    arr = data
    window_size = threshold
    i = 0
    moving_averages = []

    while i < len(arr) - window_size + 1:
        window_average = round(np.sum(arr[i:i + window_size]) / window_size, 5)
        moving_averages.append(window_average)
        i += 1

    moving_averages = np.array(moving_averages)

    return moving_averages


def set_scaler_values(ch1, ch2, ch3, ch4):
    try:
        config.CH1_SCALER = int(ch1)
        config.CH2_SCALER = int(ch2)
        config.CH3_SCALER = int(ch3)
        config.CH4_SCALER = int(ch4)
    except:
        pass


def set_samples_values(ch1_start, ch2_start, ch3_start, ch4_start, ch1_end, ch2_end, ch3_end, ch4_end):
    try:
        config.CH1_SAMPLE_START = int(ch1_start)
        config.CH2_SAMPLE_START = int(ch2_start)
        config.CH3_SAMPLE_START = int(ch3_start)
        config.CH4_SAMPLE_START = int(ch4_start)
        config.CH1_SAMPLE_END = int(ch1_end)
        config.CH2_SAMPLE_END = int(ch2_end)
        config.CH3_SAMPLE_END = int(ch3_end)
        config.CH4_SAMPLE_END = int(ch4_end)
    except:
        pass


def set_position_offsets_values(ch1, ch2, ch3, ch4):
    try:
        config.CH1_OFFSET = int(ch1)
        config.CH2_OFFSET = int(ch2)
        config.CH3_OFFSET = int(ch3)
        config.CH4_OFFSET = int(ch4)
    except:
        pass


def set_no_of_channels(channels):
    config.NO_OF_CHANNELS = int(channels)


def clear_plot(plot, canvas):
    plot.clear()
    canvas.draw()
