import os
import csv
from avro.datafile import DataFileReader
from avro.io import DatumReader
import Utility

EXECUTABLE = False
CLI = True

root, output_path = Utility.get_path(EXECUTABLE, CLI)


# Write row on csv
def write_data(_file, _data, writer):
    values = _data["values"]
    samplingFrequency = _data["samplingFrequency"]
    timestampStart = _data["timestampStart"]

    _row = [_file] + [samplingFrequency] + [timestampStart] + values

    writer.writerow(_row)


# Open file and write header
def open_file(_path, _header):
    _file = open(_path, 'w', newline='')
    _writer = csv.writer(_file)
    _writer.writerow(_header)

    return _file, _writer


# Read data
for day in next(os.walk(root))[1]:
    print(day)
    day_path = root + day + "/"
    csv_root = Utility.check_dir(output_path + 'CSV(15 min)/' + day)
    for participant in next(os.walk(day_path))[1]:
        csv_path = Utility.check_dir(csv_root + "/" + participant)
        csv_path = csv_path + participant

        # Create and open file
        header = ["filename", "samplingFrequency", "timestampStart", "[data]"]
        temperature_file, temperature_writer = open_file(csv_path + "_temperature.csv", header)
        eda_file, eda_writer = open_file(csv_path + "_eda.csv", header)
        bvp_file, bvp_writer = open_file(csv_path + "_bvp.csv", header)
        systolicPeaks_file, systolicPeaks_writer = open_file(csv_path + "_systolicPeaks.csv", ["peaksTimeNanos"])

        # Read Data
        participant_directory = day_path + participant
        if not os.path.exists(participant_directory):
            data_path = participant_directory + "/raw_data/v6/"
            for file in os.listdir(data_path):
                reader = DataFileReader(open(data_path + file, "rb"), DatumReader())

                data = []
                for datum in reader:
                    data = datum
                reader.close()
                print("Reading: ", file)

                eda = data["rawData"]["eda"]
                temperature = data["rawData"]["temperature"]
                bvp = data["rawData"]["bvp"]
                systolicPeaks = data["rawData"]["systolicPeaks"]

                # Write row
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

if EXECUTABLE:
    print("\nConversion complete")
    print("Press any key to close")
    input()
