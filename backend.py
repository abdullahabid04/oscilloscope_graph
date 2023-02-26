import pandas as pd
import numpy as np
from decimal import Decimal
from requirements import config
from utils import format_wave, get_high_low_values, remove_duplicates
from pathlib import Path
import pprint
from tkinter.filedialog import askopenfilename


def open_dataset():
    filename = askopenfilename(filetypes=[("csv files", "*.csv")])
    path_to_file = Path(filename)
    config.DATA_FRAME = pd.read_csv(path_to_file)


def calculate_cycle_time(channel, label, start, end):
    df = remove_duplicates(config.DATA_FRAME)

    time_ = list(df["Time"])
    channel_ = format_wave(df[channel])

    channel_mean = np.mean(channel_)
    channel_high, channel_low = get_high_low_values(channel_, channel_mean)

    cycle_count = 0
    count = False

    high_pulse_start, high_pulse_end = [], []
    duty_cycles_indexes = []
    duty_cycles_times = []
    duty_cycle_pairs = []

    for index, item in enumerate(channel_):
        if not count and item == channel_high:
            high_pulse_start.append(index)
            count = True
        if count and item == channel_low:
            high_pulse_end.append(index - 1)
            count = False
            cycle_count += 1

    for idx in range(cycle_count):
        duty_cycle_index = high_pulse_end[idx] - high_pulse_start[idx]
        duty_cycle_time = time_[high_pulse_end[idx]] - time_[high_pulse_start[idx]]
        duty_cycle_pair = (time_[high_pulse_start[idx]], time_[high_pulse_end[idx]])

        duty_cycles_indexes.append(duty_cycle_index)
        duty_cycles_times.append(duty_cycle_time)
        duty_cycle_pairs.append(duty_cycle_pair)

    cycle_time = duty_cycle_pairs[end][0] - duty_cycle_pairs[start][1]
    print(cycle_time)

    label.set(cycle_time)


def calculate_labels_pos(time, channel):
    time_ = time
    channel_ = format_wave(channel)

    channel_mean = np.mean(channel_)

    channel_high, channel_low = get_high_low_values(channel_, channel_mean)

    cycle_count = 0
    count = False

    high_pulse_start, high_pulse_end = [], []
    duty_cycles_indexes = []
    duty_cycles_times = []

    for index, item in enumerate(channel_):
        if not count and item == channel_high:
            high_pulse_start.append(index)
            count = True
        if count and item == channel_low:
            high_pulse_end.append(index - 1)
            count = False
            cycle_count += 1

    for idx in range(cycle_count):
        duty_cycle = high_pulse_end[idx] - high_pulse_start[idx]
        duty_cycles_indexes.append(duty_cycle)

    for idx in range(cycle_count):
        duty_cycle = Decimal(time_[high_pulse_end[idx]]) - Decimal(time_[high_pulse_start[idx]])
        duty_cycles_times.append(duty_cycle)

    pprint.pprint(duty_cycles_indexes)
    pprint.pprint(duty_cycles_times)
    pprint.pprint(cycle_count)

    return (channel_high, channel_low, cycle_count), (duty_cycles_indexes, duty_cycles_times), (
        high_pulse_start, high_pulse_end)


def get_pos_labels(time, channel, channel_high, channel_low, cycle_count, duty_cycles_indexes, duty_cycles_times,
                   high_pulse_start, high_pulse_end):
    x_indexes = []
    y_index = channel_high
    duty_cycle_labels = []
    pulse_count_labels = []

    for i in range(cycle_count):
        x_index = (high_pulse_start[i] + high_pulse_end[i]) // 2
        x_indexes.append(time[x_index])

        duty_cycle_labels.append(str(duty_cycles_indexes[i]))
        pulse_count_labels.append(str(i + 1))

    return (x_indexes, y_index), (duty_cycle_labels, pulse_count_labels)


def plot_channel(plot, time, channel, color, channel_name):
    plot.plot(time, channel, color, label=channel_name, linestyle="solid")


def plot_channel_labels(plot, label_x, label_y, duty_cycle_label, pulse_count_label):
    for index, (label_dc, label_pc) in enumerate(zip(duty_cycle_label, pulse_count_label)):
        plot.annotate(label_dc, (label_x[index], label_y), textcoords="offset pixels",
                      xytext=(0, 7), ha='center', va='center')
        plot.annotate(label_pc, (label_x[index], label_y), textcoords="offset pixels",
                      xytext=(0, -7), ha='center', va='center')


def plot_channel_1(plot, df, time_array):
    time_array_1 = time_array[config.CH1_SAMPLE_START:config.CH1_SAMPLE_END]
    channel1_list = list(
        (((df['CH1']) + config.CH1_OFFSET) * config.CH1_SCALER)[config.CH1_SAMPLE_START:config.CH1_SAMPLE_END])
    channel1_array = np.array(channel1_list)
    channel1_array = format_wave(channel1_array)
    time_array_1 = np.array(time_array_1)
    channel1_high_low_count, channel1_duty_cycles, channel1_pulses = calculate_labels_pos(time_array_1, channel1_list)
    channel1_xy_values, channel1_labels = get_pos_labels(time_array_1, channel1_array, channel1_high_low_count[0],
                                                         channel1_high_low_count[1],
                                                         channel1_high_low_count[2], channel1_duty_cycles[0],
                                                         channel1_duty_cycles[1], channel1_pulses[0],
                                                         channel1_pulses[1])
    plot_channel(plot, time_array_1, channel1_array, 'red', 'CH1')
    plot_channel_labels(plot, channel1_xy_values[0], channel1_xy_values[1], channel1_labels[0], channel1_labels[1])


def plot_channel_2(plot, df, time_array):
    time_array_2 = time_array[config.CH2_SAMPLE_START:config.CH2_SAMPLE_END]
    channel2_list = list(
        (((df['CH2']) + config.CH2_OFFSET) * config.CH2_SCALER)[config.CH2_SAMPLE_START: config.CH2_SAMPLE_END])
    channel2_array = np.array(channel2_list)
    channel2_array = format_wave(channel2_array)
    time_array_2 = np.array(time_array_2)
    channel2_high_low_count, channel2_duty_cycles, channel2_pulses = calculate_labels_pos(time_array_2, channel2_list)
    channel2_xy_values, channel2_labels = get_pos_labels(time_array_2, channel2_array, channel2_high_low_count[0],
                                                         channel2_high_low_count[1],
                                                         channel2_high_low_count[2], channel2_duty_cycles[0],
                                                         channel2_duty_cycles[1], channel2_pulses[0],
                                                         channel2_pulses[1])
    plot_channel(plot, time_array_2, channel2_array, 'green', 'CH2')
    plot_channel_labels(plot, channel2_xy_values[0], channel2_xy_values[1], channel2_labels[0], channel2_labels[1])


def plot_channel_3(plot, df, time_array):
    time_array_3 = time_array[config.CH3_SAMPLE_START:config.CH3_SAMPLE_END]
    channel3_list = list(
        (((df['CH3']) + config.CH3_OFFSET) * config.CH3_SCALER)[config.CH3_SAMPLE_START: config.CH3_SAMPLE_END])
    channel3_array = np.array(channel3_list)
    channel3_array = format_wave(channel3_array)
    time_array_3 = np.array(time_array_3)
    channel3_high_low_count, channel3_duty_cycles, channel3_pulses = calculate_labels_pos(time_array_3, channel3_list)
    channel3_xy_values, channel3_labels = get_pos_labels(time_array_3, channel3_array, channel3_high_low_count[0],
                                                         channel3_high_low_count[1],
                                                         channel3_high_low_count[2], channel3_duty_cycles[0],
                                                         channel3_duty_cycles[1], channel3_pulses[0],
                                                         channel3_pulses[1])
    plot_channel(plot, time_array_3, channel3_array, 'blue', 'CH3')
    plot_channel_labels(plot, channel3_xy_values[0], channel3_xy_values[1], channel3_labels[0], channel3_labels[1])


def plot_channel_4(plot, df, time_array):
    time_array_4 = time_array[config.CH4_SAMPLE_START:config.CH4_SAMPLE_END]
    channel4_list = list(
        (((df['CH4']) + config.CH4_OFFSET) * config.CH4_SCALER)[config.CH4_SAMPLE_START: config.CH4_SAMPLE_END])
    channel4_array = np.array(channel4_list)
    channel4_array = format_wave(channel4_array)
    time_array_4 = np.array(time_array_4)
    channel4_high_low_count, channel4_duty_cycles, channel4_pulses = calculate_labels_pos(time_array_4, channel4_list)
    channel4_xy_values, channel4_labels = get_pos_labels(time_array_4, channel4_array, channel4_high_low_count[0],
                                                         channel4_high_low_count[1],
                                                         channel4_high_low_count[2], channel4_duty_cycles[0],
                                                         channel4_duty_cycles[1], channel4_pulses[0],
                                                         channel4_pulses[1])
    plot_channel(plot, time_array_4, channel4_array, 'purple', 'CH4')
    plot_channel_labels(plot, channel4_xy_values[0], channel4_xy_values[1], channel4_labels[0], channel4_labels[1])


def plot_graph(plot, canvas, channels=0, ch1=0, ch2=0, ch3=0, ch4=0):
    df = remove_duplicates(config.DATA_FRAME)

    time_list = list(df['Time'])
    time_array = [Decimal(t) for t in time_list]

    plot_channels_functions = [plot_channel_1, plot_channel_2, plot_channel_3, plot_channel_4]
    plot_selected_channels = [ch1, ch2, ch3, ch4]

    plot.clear()

    if channels == 1:
        for idx in range(config.NO_OF_CHANNELS):
            plot_channels_functions[idx](plot, df, time_array)
    else:
        for index in range(config.NO_OF_CHANNELS):
            if plot_selected_channels[index] == 1:
                plot_channels_functions[index](plot, df, time_array)

    plot.legend(loc="upper right", prop={"size": 5}, labels=["CH1", "CH2", "CH3", "CH4"],
                labelcolor=['red', 'green', 'blue', 'black'])
    plot.grid(linestyle=":")

    canvas.draw()
