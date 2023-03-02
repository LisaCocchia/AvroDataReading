import os
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import Utility


def read_accelerometer_data(accelerometer_data, print_info):
    # Convert ADC counts in g
    delta_physical = accelerometer_data["imuParams"]["physicalMax"] - accelerometer_data["imuParams"]["physicalMin"]
    delta_digital = accelerometer_data["imuParams"]["digitalMax"] - accelerometer_data["imuParams"]["digitalMin"]
    x_g = [val * delta_physical / delta_digital for val in accelerometer_data["x"]]
    y_g = [val * delta_physical / delta_digital for val in accelerometer_data["y"]]
    z_g = [val * delta_physical / delta_digital for val in accelerometer_data["z"]]

    # Print info about data
    if print_info:
        print("Accelerometers info:")
        print("Number of samples: {}".format(len(x_g)))
        print("Duration: {} seconds".format(len(x_g) / accelerometer_data["samplingFrequency"]))
        print("X range [min, max]: [{},{}]".format(min(x_g), max(x_g)))
        print("Y range [min, max]: [{},{}]".format(min(y_g), max(y_g)))
        print("Z range [min, max]: [{},{}]".format(min(z_g), max(z_g)))
        print(" ")

    # Create time vector (in your local timezone)
    datetime_time = Utility.create_time_vector(accelerometer_data, len(x_g))

    # Plot
    plt.figure()
    plt.plot(datetime_time, x_g, label="x", linewidth=0.5)
    plt.plot(datetime_time, y_g, label="y", linewidth=0.5)
    plt.plot(datetime_time, z_g, label="z", linewidth=0.5)
    plt.ylabel("Acceleration [g]")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig('plot/accelerometer/accelerometer_' + file + '.png')
    # plt.show()


def read_temperature_data(temperature_data, print_info):
    values = temperature_data["values"]
    samplingFrequency = temperature["samplingFrequency"]

    # Print info about data
    if print_info:
        print("Temperature info:")
        print("Number of samples: {}".format(len(temperature)))
        print("Duration: {} seconds".format(len(values) / samplingFrequency))
        print(" ")

    datetime_time = Utility.create_time_vector(temperature_data, len(values))

    # Plot
    plt.figure()
    plt.plot(datetime_time, values, label="Temperature", linewidth=0.5)
    plt.ylabel("Temperature °C")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig('plot/temperature/temperature' + file + '.png')
    pass


def read_eda_data(eda_data, print_info):
    values = eda_data["values"]
    samplingFrequency = eda["samplingFrequency"]

    # Print info about data
    if print_info:
        print("Eda info:")
        print("Number of samples: {}".format(len(values)))
        print("Duration: {} seconds".format(len(values) / samplingFrequency))
        print(" ")

    datetime_time = Utility.create_time_vector(eda_data, len(values))

    # Plot
    plt.figure()
    plt.plot(datetime_time, values, label="eda", linewidth=0.5)
    plt.ylabel("Eda uS")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig('plot/eda/eda' + file + '.png')
    # plt.show()
    pass


avro_file_path = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/2023-02-10/FEDE1-3YK3K1527W/raw_data/v6/"
avro_files = os.listdir(avro_file_path)

PRINT_INFO = False

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


# Read Data
for i, file in enumerate(avro_files):

    reader = DataFileReader(open(avro_file_path + file, "rb"), DatumReader())

    data = []
    for datum in reader:
        data = datum
    reader.close()

    # Access raw data
    accelerometer = data["rawData"]["accelerometer"]
    temperature = data["rawData"]["temperature"]
    eda = data["rawData"]["eda"]

    if i == 0:
        # Print structure
        Utility.print_structure(accelerometer, "Accelerometers fields:")
        Utility.print_structure(temperature, "Temperature fields:")
        Utility.print_structure(eda, "Eda fields:")

    print("Reading: ", file)
    read_accelerometer_data(accelerometer, PRINT_INFO)
    read_temperature_data(temperature, PRINT_INFO)
    read_eda_data(eda, PRINT_INFO)
