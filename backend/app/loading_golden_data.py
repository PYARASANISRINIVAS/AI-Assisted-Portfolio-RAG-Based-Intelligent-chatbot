# loading the golden datset
import json 
with open(r"golden_dataset.json", "r", encoding="utf-8") as file:
    golden_dataset = json.load(file)
    print("Loaded the golden data succesfully ! ")