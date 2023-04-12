import csv
import os
import sys

import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Utility

EXECUTABLE = False
CLI = True

if EXECUTABLE:
    root = os.path.dirname(sys.executable) + '/'
    output_path = "../output/"
elif CLI:
    os.chdir("../participant_data")
    root = os.getcwd() + "/"
    output_path = "../output/"
else:       # LOCAL
    root = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/"
    output_path = "output/"

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


def save_plot(y, x, _path, _title):
    plt.figure()
    plt.plot(y, x, label=_title, linewidth=0.5)
    plt.ylabel(_title)
    plt.grid(True)
    plt.legend(loc="best")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m - %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=30, ha="right")
    plt.savefig(_path)
    plt.close()


def generate_plot(_path, title, _data, _round = False):
    values = _data["values"]
    if _round:
        values = Utility.round_list(values, 2)
    datetime_time = Utility.create_time_vector(_data, len(values))

    _path = Utility.check_dir(_path + title)
    _path = _path + file + '.png'

    save_plot(datetime_time, values, _path, title)


for day in next(os.walk(root))[1]:
    print(day)
    day_path = root + day + "/"

    plot_root = Utility.check_dir(output_path + 'PLOT/' + day)

    for participant in next(os.walk(day_path))[1]:
        participant_path = day_path + participant + "/raw_data/v6/"

        plot_path = Utility.check_dir(plot_root + "/" + participant)

        for i, file in enumerate(os.listdir(participant_path)):

            reader = DataFileReader(open(participant_path + file, "rb"), DatumReader())

            data = []
            for datum in reader:
                data = datum
            reader.close()

            print("Reading: ", file)
            eda = data["rawData"]["eda"]
            temperature = data["rawData"]["temperature"]
            bvp = data["rawData"]["bvp"]

            # Save plot of 15 minute charts
            generate_plot(plot_path, "Eda", eda)
            generate_plot(plot_path, "Temperature", temperature, True)
            generate_plot(plot_path, "BVP", bvp)
