from pyexcel_ods3 import get_data

data = get_data("odsWriter\Stunden April.ods")

import json

print (json.dumps(data))