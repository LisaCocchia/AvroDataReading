import os
import matplotlib.pyplot as plt
import Utility
import pandas as pd

PRINT_SCHEMA = False
PLOT = True
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


# Get values and datatime vector from avro data
def get_data(_data, _round=False):
    values = _data["values"]
    datetime_time, timeUNIX = Utility.create_time_vector(_data, len(values))
    if _round:
        values = Utility.round_list(values, 2)
    return values, datetime_time, timeUNIX


# Write the aggregated data to the CSV
def write_data_on_csv(_path, _file_name, _datetime_t, _timestamps_t, _values):
    dataFrame = pd.DataFrame({"dataTime": _datetime_t,
                              "timestamps": _timestamps_t,
                              "values": _values})
    dataFrame.to_csv(_path + _file_name, index=False)


input_root, output_root = Utility.get_path(Utility.EXECUTABLE, Utility.CLI)

for day in next(os.walk(input_root))[1]:
    print(day)
    day_path = input_root + day + "/"

    plot_root = Utility.check_dir(output_root + 'PLOT/' + day)
    csv_root = Utility.check_dir(output_root + 'CSV/' + day)

    for participant in next(os.walk(day_path))[1]:
        input_path = day_path + participant + "/raw_data/v6/"
        csv_path = csv_root + participant

        temperature_total = []
        temp_datetime_t = []
        temp_timestamps_t = []

        eda_total = []
        eda_datetime_t = []
        eda_timestamps_t = []

        bvp_total = []
        bvp_datetime_t = []
        bvp_timestamps_t = []

        systolicPeaks_total = []

        for i, file in enumerate(os.listdir(input_path)):
            print("Reading: ", file)
            eda, temperature, bvp, systolicPeaks = Utility.read_avro_data(input_path, file)

            # Get data and datatime
            eda_value, eda_datatime, eda_timestamps = get_data(eda)
            temp_value, temp_datatime, temp_timestamps = get_data(temperature, True)
            bvp_value, bvp_datatime, bvp_timestamps = get_data(bvp)

            # Aggregate data
            temp_datetime_t = Utility.concat_h(temp_datetime_t, temp_datatime)
            temp_timestamps_t = Utility.concat_h(temp_timestamps_t, temp_timestamps)
            temperature_total = Utility.concat_h(temperature_total, temp_value)

            eda_datetime_t = Utility.concat_h(eda_datetime_t, eda_datatime)
            eda_timestamps_t = Utility.concat_h(eda_timestamps_t, eda_timestamps)
            eda_total = Utility.concat_h(eda_total, eda_value)

            bvp_datetime_t = Utility.concat_h(bvp_datetime_t, bvp_datatime)
            bvp_timestamps_t = Utility.concat_h(bvp_timestamps_t, bvp_timestamps)
            bvp_total = Utility.concat_h(bvp_total, bvp_value)

            systolicPeaks_total = Utility.concat_h(systolicPeaks_total, systolicPeaks["peaksTimeNanos"])

        if PLOT:
            plot_path = Utility.check_dir(plot_root + participant)
            # Plot total session charts
            path = plot_path + '/' + "Temperature_" + participant + '.png'
            Utility.save_plot(temp_datetime_t, temperature_total, path, "Temperature_tot")
            path = plot_path + '/' + "EDA_" + participant + '.png'
            Utility.save_plot(eda_datetime_t, eda_total, path, "Eda_tot")
            path = plot_path + '/' + "BVP_" + participant + '.png'
            Utility.save_plot(bvp_datetime_t, bvp_total, path, "BVP_tot")

        # CSV
        csv_path = Utility.check_dir(csv_root + participant)

        # Write data to CSV
        write_data_on_csv(csv_path, participant + '_temperature_TOT.csv',
                          temp_datetime_t, temp_timestamps_t, temperature_total)
        write_data_on_csv(csv_path, participant + '_eda_TOT.csv',
                          eda_datetime_t, eda_timestamps_t, eda_total)
        write_data_on_csv(csv_path, participant + '_bvp_TOT.csv',
                          bvp_datetime_t, bvp_timestamps_t, bvp_total)

        dataFrame = pd.DataFrame({"peaksTimeNanos": systolicPeaks_total})
        dataFrame.to_csv(csv_path + participant + '_systolicPeaks_TOT.csv', index=False)

print("\nConversion done.")
if Utility.EXECUTABLE:
    print("Press any key to close")
    input()
