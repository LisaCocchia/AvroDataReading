import json
import os

from avro.datafile import DataFileReader
from avro.io import DatumReader
from pygments import highlight, lexers, formatters

avro_file_path = "C:/Users/lisac/Documents/Cyberduck/1/participant_data/2023-02-10/FEDE1-3YK3K1527W/raw_data/v6/"
avro_files = os.listdir(avro_file_path)
file = avro_files[1]

reader = DataFileReader(open(avro_file_path+file, "rb"), DatumReader())

# Print the Avro schema
schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
formatted_schema = json.dumps(schema, indent=3)
colorful_schema = highlight(formatted_schema, lexers.JsonLexer(), formatters.TerminalFormatter())
print(colorful_schema)
print(" ")
with open("schema_json", 'w') as f:
    f.write(formatted_schema)
