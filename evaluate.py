import json

pred = {x["id"]: x for x in json.load(open("output.json"))}
truth = {x["id"]: x for x in json.load(open("ground_truth.json"))}

fields = [
    "product_line",
    "origin_port_code",
    "origin_port_name",
    "destination_port_code",
    "destination_port_name",
    "incoterm",
    "cargo_weight_kg",
    "cargo_cbm",
    "is_dangerous"
]

correct = 0
total = 0

for id in truth:
    for f in fields:
        total += 1
        if pred[id][f] == truth[id][f]:
            correct += 1

print("Overall accuracy:", round(correct / total * 100, 2), "%")
