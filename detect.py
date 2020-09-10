import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:
    #create 3 list for each different room
    temperature_lab = []
    temperature_class = []
    temperature_office = []
    with open(file, "r") as f:
        for line in f:
            #loading the lines of data, then separating each data line based on room
            r = json.loads(line)
            try:
                temp = (r['lab1']['temperature'][0]);
                temperature_lab.append(temp) #if above line works, add to lab list
            except:
                pass
            try:
                temp = (r['office']['temperature'][0]);
                temperature_office.append(temp) #if above line works, add to office list
            except:
                pass
            try:
                temp = (r['class1']['temperature'][0]);
                temperature_class.append(temp) #if above line works, add to class list
            except:
                pass

    #calculating standard deviation and mean of lab, then printing
    standev_lab = np.std(temperature_lab)
    mean_lab = np.mean(temperature_lab)
    print ("Standard Deviation of Lab :", standev_lab)
    print ("Average of Lab:", mean_lab, "\n")

    #calculating standard deviation and mean of class, then printing
    standev_class = np.std(temperature_class)
    mean_class = np.mean(temperature_class)
    print ("Standard Deviation of Class :", standev_class)
    print ("Average of Class:", mean_class, "\n")

    #calculating standard deviation and mean of office, then printing
    standev_office = np.std(temperature_office)
    mean_office = np.mean(temperature_office)
    print ("Standard Deviation of Office :", standev_office)
    print ("Average of Office:", mean_office, "\n")

    #finding the length of each temperature list as data is different for each person
    len_lab = len(temperature_lab);
    len_office = len(temperature_office);
    len_class = len(temperature_class);

    #run a for loop on each temperature list to find anomalies within each one
    #our condition is that the temperature should stay within the mean +/- 2 standard deviations
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
