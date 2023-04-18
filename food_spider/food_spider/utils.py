
import json

def load_output(infile):
    products = []
    with open(infile) as f:
        for line in f:
            line = line.rstrip("\n")
            line = line.rstrip(",")
            line = line.rstrip("[")
            line = line.rstrip("]")
            if (line == "[") | (line == "]") | (line == "]["):
                continue
            if (line == ""):
                continue
            products.append(json.loads(line))
    return products