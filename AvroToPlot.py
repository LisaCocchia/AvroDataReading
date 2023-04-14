import os
import matplotlib.pyplot as plt
import Utility

EXECUTABLE = False
CLI = False


def generate_plot(_path, _title, _data, _file_name, _round=False):
    _values = _data["values"]
    if _round:
        _values = Utility.round_list(_values, 2)
    _datetime_time = Utility.create_time_vector(_data, len(_values))

    # _path: output_root/PLOT/data/participant/dataType/avroFileName.png
    _path = Utility.check_dir(_path + _title)
    _path = _path + _file_name + '.png'

    Utility.save_plot(_datetime_time, _values, _path, _title)
    return


print("AvroToPlot.py is running\n")
input_root, output_root = Utility.get_path(EXECUTABLE, CLI)

# dpi of plot image
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

for day in next(os.walk(input_root))[1]:
    print(day)
    day_path = input_root + day + "/"
    plot_root = Utility.check_dir(output_root + 'PLOT/' + day)

    # for all participant folder in day_path
    for participant in next(os.walk(day_path))[1]:
        # plot_path: output_root/PLOT/day/participant
        plot_path = plot_root + participant

        if os.path.exists(plot_path):
            print("The folder of " + participant + " already exists.")
        else:
            # input_path: root_/day/participant/raw_data/v6/
            input_path = day_path + participant + "/raw_data/v6/"

            for i, file in enumerate(os.listdir(input_path)):
                print("Reading: ", file)
                eda, temperature, bvp, _ = Utility.read_avro_data(input_path, file)

                # Save plot of 15 minute charts
                plot_path = Utility.check_dir(plot_path)
                file_name = Utility.remove_ext(file)
                generate_plot(plot_path, "Eda", eda, file_name)
                generate_plot(plot_path, "Temperature", temperature, file_name, True)
                generate_plot(plot_path, "BVP", bvp, file_name)

if EXECUTABLE:
    print("\nConversion complete")
    print("Press any key to close")
    input()
else:
    print("\nAvroToPlot DONE")