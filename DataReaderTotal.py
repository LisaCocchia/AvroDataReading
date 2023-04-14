import csv
import os
import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Utility

EXECUTABLE = False
CLI = False

PRINT_SCHEMA = False
PLOT = True
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


# Get values and datatime vector from avro data
def get_data(_data, _round=False):
    values = _data["values"]
    datetime_time = Utility.create_time_vector(_data, len(values))
    if _round:
        values = Utility.round_list(values, 2)

    return values, datetime_time


# Write the aggregated data to the CSV
def write_data_on_csv(_path, _header, _data):
    _file = open(_path, 'w', newline='')
    writer = csv.writer(_file)
    writer.writerow(_header)
    writer.writerow(_data)
    _file.close()


input_root, output_root = Utility.get_path(EXECUTABLE, CLI)

for day in next(os.walk(input_root))[1]:
    print(day)
    day_path = input_root + day + "/"

    plot_root = Utility.check_dir(output_root + 'PLOT/' + day)
    csv_root = Utility.check_dir(output_root + 'CSV/' + day)

    for participant in next(os.walk(day_path))[1]:
        input_path = day_path + participant + "/raw_data/v6/"
        plot_path = Utility.check_dir(plot_root + participant)
        csv_path = Utility.check_dir(csv_root + participant)

        if os.path.exists(csv_path):
            print("The folder of " + participant + " already exists.")
        else:

            temperature_total = []
            temp_datetime_t = []
            eda_total = []
            eda_datetime_t = []
            bvp_total = []
            bvp_datetime_t = []
            systolicPeaks_total = []

            for i, file in enumerate(os.listdir(input_path)):
                print("Reading: ", file)
                eda, temperature, bvp, systolicPeaks = Utility.read_avro_data(input_path, file)

                if i == 0:
                    # Data info for CSV
                    eda_info = [eda["samplingFrequency"], eda["timestampStart"]]
                    temperature_info = [temperature["samplingFrequency"], temperature["timestampStart"]]
                    bvp_info = [bvp["samplingFrequency"], bvp["timestampStart"]]

                # Get data and datatime
                eda_value, eda_datatime = get_data(eda)
                temp_value, temp_datatime = get_data(temperature, True)
                bvp_value, bvp_datatime = get_data(bvp)

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
                Utility.save_plot(temp_datetime_t, temperature_total, path, "Temperature_tot")
                path = plot_path + '/' + "EDA_" + participant + '.png'
                Utility.save_plot(eda_datetime_t, eda_total, path, "Eda_tot")
                path = plot_path + '/' + "BVP_" + participant + '.png'
                Utility.save_plot(bvp_datetime_t, bvp_total, path, "BVP_tot")

            # CSV
            header = ["samplingFrequency", "timestampStart", "[data]"]

            write_data_on_csv(csv_path + '_temperature_TOT.csv', header,
                              Utility.concat_h(np.array(temperature_info), temperature_total))
            write_data_on_csv(csv_path + '_eda_TOT.csv', header, Utility.concat_h(np.array(eda_info), eda_total))
            write_data_on_csv(csv_path + '_bvp_TOT.csv', header, Utility.concat_h(np.array(bvp_info), bvp_total))
            write_data_on_csv(csv_path + '_systolicPeaks_TOT.csv', "peaksTimeNanos", systolicPeaks_total)
