import csv
import os
import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Utility

EXECUTABLE = False
CLI = True
PRINT_SCHEMA = False
PRINT_DATA_INFO = False
PLOT = True
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

root, output_path = Utility.get_path(EXECUTABLE, CLI)


def save_plot(y, x, path, title):
    # Plot
    plt.figure()
    plt.plot(y, x, label=title, linewidth=0.5)
    plt.ylabel(title)
    plt.grid(True)
    plt.legend(loc="best")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m - %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=30, ha="right")
    plt.savefig(path)
    plt.close()


def get_data_file(_data, print_info=False, _round=False):
    values = _data["values"]
    samplingFrequency = _data["samplingFrequency"]
    # Print info about data
    if print_info:
        print("Temperature info:")
        print("Number of samples: {}".format(len(_data)))
        print("Duration: {} seconds".format(len(values) / samplingFrequency))
        print(" ")

    datetime_time = Utility.create_time_vector(_data, len(values))

    if _round:
        values = Utility.round_list(values, 2)
    return values, datetime_time


def plot_data(_path, title, _data, datetime_time):
    _path = Utility.check_dir(_path + title)
    _path = _path + file + '.png'

    save_plot(datetime_time, _data, _path, title)


def write_csv(_path, _header, _data):
    _file = open(_path, 'w', newline='')
    writer = csv.writer(_file)
    writer.writerow(_header)
    writer.writerow(_data)
    _file.close()


for day in next(os.walk(root))[1]:
    print(day)
    file_path = root + day + "/"

    plot_root = Utility.check_dir(output_path + 'PLOT/' + day)
    csv_root = Utility.check_dir(output_path + 'CSV/' + day)

    for participant in next(os.walk(file_path))[1]:
        avro_file_path = file_path + participant + "/raw_data/v6/"

        plot_path = Utility.check_dir(plot_root + "/" + participant)

        temperature_total = []
        temp_datetime_t = []
        eda_total = []
        eda_datetime_t = []
        bvp_total = []
        bvp_datetime_t = []
        systolicPeaks_total = []

        for i, file in enumerate(os.listdir(avro_file_path)):
            reader = DataFileReader(open(avro_file_path + file, "rb"), DatumReader())

            if PRINT_SCHEMA and i == 0:
                Utility.print_avro_schema(reader)
            data = []
            for datum in reader:
                data = datum
            reader.close()

            print("Reading: ", file)
            eda = data["rawData"]["eda"]
            temperature = data["rawData"]["temperature"]
            bvp = data["rawData"]["bvp"]
            systolicPeaks = data["rawData"]["systolicPeaks"]

            if i == 0:
                # Print structure
                if PRINT_DATA_INFO:
                    Utility.print_structure(temperature, "Temperature fields:")
                    Utility.print_structure(eda, "Eda fields:")

                # Data info for CSV
                eda_info = [eda["samplingFrequency"], eda["timestampStart"]]
                temperature_info = [temperature["samplingFrequency"], temperature["timestampStart"]]
                bvp_info = [bvp["samplingFrequency"], bvp["timestampStart"]]

            # Get data and datatime
            eda_value, eda_datatime = get_data_file(eda, PRINT_DATA_INFO)
            temp_value, temp_datatime = get_data_file(temperature, PRINT_DATA_INFO, True)
            bvp_value, bvp_datatime = get_data_file(bvp, PRINT_DATA_INFO)

            # # Plot 15 minute charts
            # plot_data(plot_path, "Eda", eda_value, eda_datatime)
            # plot_data(plot_path, "Temperature", temp_value, temp_datatime)
            # plot_data(plot_path, "BVP", bvp_value, bvp_datatime)

            # Aggregate data
            temp_datetime_t = Utility.concat_h(temp_datetime_t, temp_datatime)
            temperature_total = Utility.concat_h(temperature_total, temp_value)

            eda_datetime_t = Utility.concat_h(eda_datetime_t, eda_datatime)
            eda_total = Utility.concat_h(eda_total, eda_value)

            bvp_datetime_t = Utility.concat_h(bvp_datetime_t, bvp_datatime)
            bvp_total = Utility.concat_h(bvp_total, bvp_value)

            systolicPeaks_total = Utility.concat_h(systolicPeaks_total, systolicPeaks["peaksTimeNanos"])

        if PLOT:
            # Plot total session charts
            path = plot_path + '/' + "Temperature_" + participant + '.png'
            save_plot(temp_datetime_t, temperature_total, path, "Temperature_tot")
            path = plot_path + '/' + "EDA_" + participant + '.png'
            save_plot(eda_datetime_t, eda_total, path, "Eda_tot")
            path = plot_path + '/' + "BVP_" + participant + '.png'
            save_plot(bvp_datetime_t, bvp_total, path, "BVP_tot")

        # CSV
        csv_path = Utility.check_dir(csv_root + "/" + participant)
        csv_path = csv_path + participant

        header = ["samplingFrequency", "timestampStart", "[data]"]

        write_csv(csv_path + '_temperature_TOT.csv', header,
                  Utility.concat_h(np.array(temperature_info), temperature_total))
        write_csv(csv_path + '_eda_TOT.csv', header, Utility.concat_h(np.array(eda_info), eda_total))
        write_csv(csv_path + '_bvp_TOT.csv', header, Utility.concat_h(np.array(bvp_info), bvp_total))
        write_csv(csv_path + '_systolicPeaks_TOT.csv', "peaksTimeNanos", systolicPeaks_total)
