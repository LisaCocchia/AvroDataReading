import os
import csv
import numpy as np
from avro.datafile import DataFileReader
from avro.io import DatumReader


def write_data(data, writer):
    values = data["values"]
    samplingFrequency = data["samplingFrequency"]
    timestampStart = data["timestampStart"]

    row = np.concatenate((samplingFrequency, timestampStart, values), axis=None)
    writer.writerow(row)


avro_file_path = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/2023-02-10/FEDE1-3YK3K1527W/raw_data/v6/"
avro_files = os.listdir(avro_file_path)

temperature_file = open('CSV/_temperature.csv', 'w', newline='')
temperature_writer = csv.writer(temperature_file)

eda_file = open('CSV/_eda.csv', 'w', newline='')
eda_writer = csv.writer(eda_file)

bvp_file = open('CSV/_bvp.csv', 'w', newline='')
bvp_writer = csv.writer(bvp_file)

systolicPeaks_file = open('CSV/_systolicPeaks.csv', 'w', newline='')
systolicPeaks_writer = csv.writer(systolicPeaks_file)

# Read Data
for i, file in enumerate(avro_files):

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

    write_data(eda, eda_writer)
    write_data(temperature, temperature_writer)
    write_data(bvp, bvp_writer)

    timestamp = systolicPeaks["peaksTimeNanos"]
    systolicPeaks_writer.writerow(timestamp)

temperature_file.close()
eda_file.close()
bvp_file.close()
systolicPeaks_file.close()
