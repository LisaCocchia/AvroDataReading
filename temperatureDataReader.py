import os
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
from datetime import datetime


avro_file_path = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/2023-02-10/FEDE1-3YK3K1527W/raw_data/v6/"
avro_files = os.listdir(avro_file_path)


# Read Avro file
for i, file in enumerate(avro_files):

    reader = DataFileReader(open(avro_file_path+file, "rb"), DatumReader())

    data = []
    for datum in reader:
        data = datum
    reader.close()

    # Plot temperature #
    # Access temperature raw data
    acc = data["rawData"]["temperature"]

    if i == 0:
       # Print structure
        print("Temperature fields:")
        for key, val in acc.items():
            print("- " + key)
            if type(val) is dict:
                for k in val.keys():
                    print(" - " + k)
        print(" ")

    values = acc["values"]
    samplingFrequency = acc["samplingFrequency"]

    # Print info about data
    print("Reading: ", file)
    print("Temperature info:")
    print("Number of samples: {}".format(len(values)))
    print("Duration: {} seconds".format(len(values) / samplingFrequency))
    print(" ")

    # Create time vector (in your local timezone)
    startSeconds = acc["timestampStart"] / 1000000
    timeSeconds = list(range(0, len(values)))
    timeUNIX = [t / acc["samplingFrequency"] + startSeconds for t in timeSeconds]
    datetime_time = [datetime.fromtimestamp(x) for x in timeUNIX]

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    # Plot
    plt.figure()

    #plt(datetime_time, values, label="value")
    plt.plot(datetime_time, values, label="temperature", linewidth=0.5)
    plt.ylabel("Temperature")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig('plot/temperature/temperature' + file + '.png')
    #plt.show()

