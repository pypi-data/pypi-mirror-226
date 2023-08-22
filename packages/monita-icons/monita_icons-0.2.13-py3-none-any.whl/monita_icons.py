import os
import json
f = open(os.path.join(os.path.expanduser( '~' ), '.local', 'vendor_map.json'))
vendor_map = json.load(f)
f.close()
