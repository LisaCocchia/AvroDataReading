import os
import csv
from avro.datafile import DataFileReader
from avro.io import DatumReader

import Utility


def write_data(file, data, writer):
    values = data["values"]
    samplingFrequency = data["samplingFrequency"]
    timestampStart = data["timestampStart"]

    _row = [file] + [samplingFrequency] + [timestampStart] + values

    writer.writerow(_row)


root = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/"
# root = "C:/Users/lisac/OneDrive - Università degli Studi di Milano-Bicocca/Magistrale/Tesi magistrale/
# Empatica-Roberto Crotti/participant_data/"
output_path = "output/"
# output_path = "C:/Users/lisac/Desktop/output/"

for day in os.listdir(root):
    file_path = root + day + "/"
    participants = os.listdir(file_path)
    csv_root = Utility.check_dir(output_path + 'CSV(15 min)/' + day)

    for participant in participants:
        avro_file_path = file_path + participant + "/raw_data/v6/"

        csv_path = Utility.check_dir(csv_root + "/" + participant)
        csv_path = csv_path + participant

        # OPEN FILE
        header = ["filename", "samplingFrequency", "timestampStart", "[data]"]
        temperature_file = open(csv_path + '_temperature.csv', 'w', newline='')
        temperature_writer = csv.writer(temperature_file)
        temperature_writer.writerow(header)

        eda_file = open(csv_path + '_eda.csv', 'w', newline='')
        eda_writer = csv.writer(eda_file)
        eda_writer.writerow(header)

        bvp_file = open(csv_path + '_bvp.csv', 'w', newline='')
        bvp_writer = csv.writer(bvp_file)
        bvp_writer.writerow(header)

        systolicPeaks_file = open(csv_path + '_systolicPeaks.csv', 'w', newline='')
        systolicPeaks_writer = csv.writer(systolicPeaks_file)
        systolicPeaks_writer.writerow("peaksTimeNanos")

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
