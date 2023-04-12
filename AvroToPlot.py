import os
import sys
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Utility

EXECUTABLE = False
CLI = True

root, output_path = Utility.get_path(EXECUTABLE, CLI)

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
        plot_path = Utility.check_dir(plot_root + "/" + participant)

        participant_directory = day_path + participant
        if not os.path.exists(participant_directory):
            data_path = participant_directory + "/raw_data/v6/"
            for i, file in enumerate(os.listdir(data_path)):

                reader = DataFileReader(open(data_path + file, "rb"), DatumReader())

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
