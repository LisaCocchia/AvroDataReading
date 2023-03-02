@staticmethod
def print_structure(data, text):
    print(text)
    for key, val in data.items():
        print("- " + key)
        if type(val) is dict:
            for k in val.keys():
                print(" - " + k)
    print(" ")