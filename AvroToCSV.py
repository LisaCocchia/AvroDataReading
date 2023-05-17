import os
import csv
import Utility


# Write row on csv
def write_row(_file, _data, _writer):
    _values = _data["values"]
    _samplingFrequency = _data["samplingFrequency"]
    _timestampStart = _data["timestampStart"]

    _row = [_file] + [_samplingFrequency] + [_timestampStart] + _values

    _writer.writerow(_row)


# Open file and write header
def open_file(_path, _file_name, _header):
    _file = open(_path + _file_name, 'w', newline='')
    _writer = csv.writer(_file)
    _writer.writerow(_header)

    return _file, _writer


print("AvroToCSV.py is running\n")
input_root, output_root = Utility.get_path(Utility.EXECUTABLE, Utility.CLI)

for day in next(os.walk(input_root))[1]:
    print(day)
    day_path = input_root + day + "/"
    csv_root = Utility.check_dir(output_root + 'CSV(15 min)/' + day)

    # for all participant folder in day_path
    for participant in next(os.walk(day_path))[1]:
        # csv_path: output/CSV(15 min)/day/participant/
        csv_path = csv_root + participant

        if os.path.exists(csv_path):
            print("The folder of " + participant + " already exists.")
        else:
            csv_path = Utility.check_dir(csv_path)

            # Create and open CSV file
            header = ["filename", "samplingFrequency", "timestampStart", "[data]"]
            temperature_file, temperature_writer = open_file(csv_path, participant + "_temperature.csv", header)
            eda_file, eda_writer = open_file(csv_path, participant + "_eda.csv", header)
            bvp_file, bvp_writer = open_file(csv_path, participant + "_bvp.csv", header)
            systolicPeaks_file, systolicPeaks_writer = \
                open_file(csv_path, participant + "_systolicPeaks.csv", ["filename",  "peaksTimeNanos"])

            # input_path: root_/day/participant/raw_data/v6/
            input_path = day_path + participant + "/raw_data/v6/"

            for file in os.listdir(input_path):
                print("Reading: ", file)
                eda, temperature, bvp, systolicPeaks = Utility.read_avro_data(input_path, file)
                print(eda)
                input()
                # Write row on CSV file
                write_row(file, eda, eda_writer)
                write_row(file, temperature, temperature_writer)
                write_row(file, bvp, bvp_writer)
                timestamp = systolicPeaks["peaksTimeNanos"]
                row = [file] + timestamp
                systolicPeaks_writer.writerow(row)

            # Close all CSV file
            temperature_file.close()
            eda_file.close()
            bvp_file.close()
            systolicPeaks_file.close()

print("\nCSV conversion done.")
if Utility.EXECUTABLE:
    print("Press any key to close")
    input()
