import csv
import os
import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Utility


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


def plot_data_file(data, print_info, title, path):
    values = data["values"]
    samplingFrequency = data["samplingFrequency"]
    # Print info about data
    if print_info:
        print("Temperature info:")
        print("Number of samples: {}".format(len(data)))
        print("Duration: {} seconds".format(len(values) / samplingFrequency))
        print(" ")

    datetime_time = Utility.create_time_vector(data, len(values))

    if PLOT:
        path = path + '/' + title
        Utility.check_dir(path)
        path = path + '/' + title + file + '.png'

        save_plot(datetime_time, values, path, title)

    return values, datetime_time


root = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/"
# root = "C:/Users/lisac/OneDrive - Università degli Studi di Milano-Bicocca/Magistrale/Tesi " \
#        "magistrale/Empatica-Roberto Crotti/participant_data/"

PRINT_INFO = False
PLOT = True
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

for day in os.listdir(root):
    file_path = root + day + "/"
    participants = os.listdir(file_path)
    for participant in participants:
        avro_file_path = file_path + participant + "/raw_data/v6/"

        plot_path = 'PLOT/' + day + "/" + participant
        Utility.check_dir(plot_path)

        temperature_total = []
        temp_datetime_t = []
        eda_total = []
        eda_datetime_t = []
        bvp_total = []
        bvp_datetime_t = []
        systolicPeaks_total = []

        for i, file in enumerate(os.listdir(avro_file_path)):

            reader = DataFileReader(open(avro_file_path + file, "rb"), DatumReader())

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
                if PRINT_INFO:
                    Utility.print_structure(temperature, "Temperature fields:")
                    Utility.print_structure(eda, "Eda fields:")
                eda_info = [eda["samplingFrequency"], eda["timestampStart"]]
                temperature_info = [temperature["samplingFrequency"], temperature["timestampStart"]]
                bvp_info = [bvp["samplingFrequency"], bvp["timestampStart"]]

            eda_value, eda_datatime = plot_data_file(eda, PRINT_INFO, "Eda", plot_path)
            temp_value, temp_datatime = plot_data_file(temperature, PRINT_INFO, "Temperature", plot_path)
            bvp_value, bvp_datatime = plot_data_file(bvp, PRINT_INFO, "BVP", plot_path)

            temp_datetime_t = Utility.concat_h(temp_datetime_t, temp_datatime)
            temperature_total = Utility.concat_h(temperature_total, temp_value)

            eda_datetime_t = Utility.concat_h(eda_datetime_t, eda_datatime)
            eda_total = Utility.concat_h(eda_total, eda_value)

            bvp_datetime_t = Utility.concat_h(bvp_datetime_t, bvp_datatime)
            bvp_total = Utility.concat_h(bvp_total, bvp_value)

            systolicPeaks_total = Utility.concat_h(systolicPeaks_total, systolicPeaks["peaksTimeNanos"])

        if PLOT:
            # Plot
            path = plot_path + '/' + "Temperature_" + participant + '.png'
            save_plot(temp_datetime_t, temperature_total, path, "Temperature_tot")
            path = plot_path + '/' + "EDA_" + participant + '.png'
            save_plot(eda_datetime_t, eda_total, path, "Eda_tot")
            path = plot_path + '/' + "BVP_" + participant + '.png'
            save_plot(bvp_datetime_t, bvp_total, path, "BVP_tot")

        # CSV
        Utility.check_dir('CSV/' + day)
        participant_folder = 'CSV/' + day + "/" + participant
        Utility.check_dir(participant_folder)
        csv_path = participant_folder + "/" + participant

        header = ["samplingFrequency", "timestampStart", "[data]"]

        temperature_file = open(csv_path + '_temperature_TOT.csv', 'w', newline='')
        temperature_writer = csv.writer(temperature_file)
        temperature_writer.writerow(header)
        temperature_writer.writerow(Utility.concat_h(np.array(temperature_info), eda_total))

        eda_file = open(csv_path + '_eda_TOT.csv', 'w', newline='')
        eda_writer = csv.writer(eda_file)
        eda_writer.writerow(header)
        eda_writer.writerow(Utility.concat_h(np.array(eda_info), eda_total))

        bvp_file = open(csv_path + '_bvp_TOT.csv', 'w', newline='')
        bvp_writer = csv.writer(bvp_file)
        bvp_writer.writerow(header)
        bvp_writer.writerow(Utility.concat_h(np.array(bvp_info), bvp_total))

        systolicPeaks_file = open(csv_path + '_systolicPeaks_TOT.csv', 'w', newline='')
        systolicPeaks_writer = csv.writer(systolicPeaks_file)
        systolicPeaks_writer.writerow("peaksTimeNanos")
        systolicPeaks_writer.writerow(systolicPeaks_total)
