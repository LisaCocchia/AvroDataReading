from datetime import datetime


@staticmethod
def print_structure(data, text):
    print(text)
    for key, val in data.items():
        print("- " + key)
        if type(val) is dict:
            for k in val.keys():
                print(" - " + k)
    print(" ")


@staticmethod
def create_time_vector(data, length):
    # Create time vector (in your local timezone)
    startSeconds = data["timestampStart"] / 1000000
    timeSeconds = list(range(0, length))
    timeUNIX = [t / data["samplingFrequency"] + startSeconds for t in timeSeconds]
    datetime_time = [datetime.fromtimestamp(x) for x in timeUNIX]

    return datetime_time
