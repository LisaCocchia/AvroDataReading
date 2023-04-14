import json
import os
import sys
from datetime import datetime

import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader
from matplotlib import pyplot as plt, dates
from pygments import highlight, formatters, lexers


def read_avro_data(input_path, file, PRINT_SCHEMA=False):
    reader = DataFileReader(open(input_path + file, "rb"), DatumReader())
    if PRINT_SCHEMA:
        print_avro_schema(reader)
    data = []
    for datum in reader:
        data = datum
    reader.close()

    eda = data['rawData']['eda']
    temperature = data['rawData']['temperature']
    bvp = data['rawData']['bvp']
    systolicPeaks = data['rawData']['systolicPeaks']

    return eda, temperature, bvp, systolicPeaks


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


def print_avro_schema(reader):
    # Print the Avro schema
    schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
    formatted_schema = json.dumps(schema, indent=3)
    colorful_schema = highlight(formatted_schema, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_schema)
    print(" ")
    with open("schema_json", 'w') as f:
        f.write(formatted_schema)


def get_path(EXECUTABLE, CLI):
    if EXECUTABLE:
        input_root = os.path.dirname(sys.executable) + '/'
        output_root = "../output/"
    elif CLI:
        os.chdir("../participant_data")
        input_root = os.getcwd() + "/"
        output_root = "../output/"
    else:  # LOCAL
        input_root = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/"
        input_root = "C:/Users/lisac/Desktop/TEST PyhtonScript/participant_data/"
        output_root = "output/"
    return input_root, output_root


def remove_ext(file_name):
    return os.path.splitext(file_name)[0]


# Create and save plot
def save_plot(_y, _x, _path, _title):
    plt.figure()
    plt.plot(_y, _x, label=_title, linewidth=0.5)
    plt.ylabel(_title)
    plt.grid(True)
    plt.legend(loc="best")
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d/%m - %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=30, ha="right")
    plt.savefig(_path)
    plt.close()
    return
