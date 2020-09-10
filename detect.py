import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:
    temperature_lab = []
    temperature_class = []
    temperature_office = []
    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            try:
                temp = (r['lab1']['temperature'][0]);
                temperature_lab.append(temp)
            except:
                pass
            try:
                temp = (r['office']['temperature'][0]);
                temperature_office.append(temp)
            except:
                pass
            try:
                temp = (r['class1']['temperature'][0]);
                temperature_class.append(temp)
            except:
                pass

    standev_lab = np.std(temperature_lab)
    mean_lab = np.mean(temperature_lab)
    print ("Standard Deviation of Lab :", standev_lab)
    print ("Average of Lab:", mean_lab, "\n")

    standev_class = np.std(temperature_class)
    mean_class = np.mean(temperature_class)
    print ("Standard Deviation of Class :", standev_class)
    print ("Average of Class:", mean_class, "\n")

    standev_office = np.std(temperature_office)
    mean_office = np.mean(temperature_office)
    print ("Standard Deviation of Office :", standev_office)
    print ("Average of Office:", mean_office, "\n")

    len_lab = len(temperature_lab);
    len_office = len(temperature_office);
    len_class = len(temperature_class);

    for x in range (1,len_lab):
        if (temperature_lab[x] > (((2 * (standev_lab)) + mean_lab) or temperature_lab[x] < (mean_lab - (2 * (standev_lab))))):
            print("The", x, "frame of the lab is an anomoly.")

    for x in range (1,len_office):
        if (temperature_office[x] > (((2 * (standev_office)) + mean_office) or temperature_office[x] < (mean_office - (2 * (standev_office))))):
            print("The", x, "frame of the office is an anomoly.")

    for x in range (1,len_class):
        if (temperature_class[x] > (((2 * (standev_class)) + mean_class) or temperature_class[x] < (mean_class - (2 * (standev_class))))):
            print("The", x, "frame of the class is an anomoly.")            


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    load_data(file)
