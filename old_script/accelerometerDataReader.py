import os
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
from datetime import datetime

import Utility

avro_file_path = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/2023-02-10/FEDE1-3YK3K1527W/raw_data/v6/"
avro_files = os.listdir(avro_file_path)


# Read Avro file
for i, file in enumerate(avro_files):

    reader = DataFileReader(open(avro_file_path+file, "rb"), DatumReader())

    data = []
    for datum in reader:
        data = datum
    reader.close()

    # Plot accelerometers #
    # Access accelerometer raw data
    acc = data["rawData"]["accelerometer"]

    if i == 0:
        # Print structure
        Utility.print_structure(acc, "Accelerometers fields:")

    # Convert ADC counts in g
    delta_physical = acc["imuParams"]["physicalMax"] - acc["imuParams"]["physicalMin"]
    delta_digital = acc["imuParams"]["digitalMax"] - acc["imuParams"]["digitalMin"]
    x_g = [val * delta_physical / delta_digital for val in acc["x"]]
    y_g = [val * delta_physical / delta_digital for val in acc["y"]]
    z_g = [val * delta_physical / delta_digital for val in acc["z"]]

    # Print info about data
    print("Reading: ", file)
    print("Accelerometers info:")
    print("Number of samples: {}".format(len(x_g)))
    print("Duration: {} seconds".format(len(x_g) / acc["samplingFrequency"]))
    print("X range [min, max]: [{},{}]".format(min(x_g), max(x_g)))
    print("Y range [min, max]: [{},{}]".format(min(y_g), max(y_g)))
    print("Z range [min, max]: [{},{}]".format(min(z_g), max(z_g)))
    print(" ")

    # Create time vector (in your local timezone)
    startSeconds = acc["timestampStart"] / 1000000
    timeSeconds = list(range(0, len(x_g)))
    timeUNIX = [t / acc["samplingFrequency"] + startSeconds for t in timeSeconds]
    datetime_time = [datetime.fromtimestamp(x) for x in timeUNIX]

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    # Plot
    plt.figure()
    plt.plot(datetime_time, x_g, label="x", linewidth=0.5)
    plt.plot(datetime_time, y_g, label="y", linewidth=0.5)
    plt.plot(datetime_time, z_g, label="z", linewidth=0.5)
    plt.ylabel("Acceleration [g]")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig('plot/accelerometer/accelerometer_'+file+'.png')
    # plt.show()






