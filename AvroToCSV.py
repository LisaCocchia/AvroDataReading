import os
import csv
from avro.datafile import DataFileReader
from avro.io import DatumReader

import Utility


def write_data(file, data, writer):
    values = data["values"]
    samplingFrequency = data["samplingFrequency"]
    timestampStart = data["timestampStart"]

    row = [file] + [samplingFrequency] + [timestampStart] + values

    writer.writerow(row)


root = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/"

for day in os.listdir(root):
    file_path = root + day + "/"
    participants = os.listdir(file_path)
    for participant in participants:
        avro_file_path = file_path + participant + "/raw_data/v6/"

        Utility.check_dir('CSV/' + day)
        csv_path = 'CSV/' + day + "/" + participant

        # OPEN FILE
        temperature_file = open(csv_path + '_temperature.csv', 'w', newline='')
        temperature_writer = csv.writer(temperature_file)

        eda_file = open(csv_path + '_eda.csv', 'w', newline='')
        eda_writer = csv.writer(eda_file)

        bvp_file = open(csv_path + '_bvp.csv', 'w', newline='')
        bvp_writer = csv.writer(bvp_file)

        systolicPeaks_file = open(csv_path + '_systolicPeaks.csv', 'w', newline='')
        systolicPeaks_writer = csv.writer(systolicPeaks_file)

        # Read Data
        for file in os.listdir(avro_file_path):

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

            write_data(file, eda, eda_writer)
            write_data(file, temperature, temperature_writer)
            write_data(file, bvp, bvp_writer)

            timestamp = systolicPeaks["peaksTimeNanos"]
            row = [file] + timestamp
            systolicPeaks_writer.writerow(timestamp)

        temperature_file.close()
        eda_file.close()
        bvp_file.close()
        systolicPeaks_file.close()
