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

    reader = DataFileReader(open(avro_file_path + file, "rb"), DatumReader())

    data = []
    for datum in reader:
        data = datum
    reader.close()

    # Plot temperature #
    # Access temperature raw data
    eda = data["rawData"]["eda"]

    if i == 0:
        # Print structure
        Utility.print_structure(eda, "Eda fields:")

    values = eda["values"]
    samplingFrequency = eda["samplingFrequency"]

    # Print info about data
    print("Reading: ", file)
    print("Eda info:")
    print("Number of samples: {}".format(len(values)))
    print("Duration: {} seconds".format(len(values) / samplingFrequency))
    print(" ")

    # Create time vector (in your local timezone)
    startSeconds = eda["timestampStart"] / 1000000
    timeSeconds = list(range(0, len(values)))
    timeUNIX = [t / eda["samplingFrequency"] + startSeconds for t in timeSeconds]
    datetime_time = [datetime.fromtimestamp(x) for x in timeUNIX]

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    # Plot
    plt.figure()

    # plt(datetime_time, values, label="value")
    plt.plot(datetime_time, values, label="eda", linewidth=0.5)
    plt.ylabel("Eda uS")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig('plot/eda/eda' + file + '.png')
    # plt.show()