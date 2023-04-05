import os
from datetime import datetime

import numpy as np


@staticmethod
def print_structure(data, text):
    print(text)
    for key, val in data.items():
        print("- " + key)
        if type(val) is dict:
            for k in val.keys():
                print(" - " + k)
    print(" ")


@staticmethod
def create_time_vector(data, length):
    # Create time vector (in your local timezone)
    startSeconds = data["timestampStart"] / 1000000
    timeSeconds = list(range(0, length))
    timeUNIX = [t / data["samplingFrequency"] + startSeconds for t in timeSeconds]
    datetime_time = [datetime.fromtimestamp(x) for x in timeUNIX]

    return datetime_time


def check_dir(directory):
    # directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory + "/"


def concat_h(a, b):
    return np.concatenate((a, b), axis=None)


def round_list(_list, decimal):
    np_array = np.array(_list)
    np_round = np.around(np_array, decimal)
    rounded_list = list(np_round)
    return rounded_list