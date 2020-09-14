#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])
            #print(time)

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

    for k in data:
        # data[k].plot()
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")

        # find the median and variance of all sensors in lab1
        print("Sensor: ", k);
        #print(data[k].mean());
        #print(data[k].std());
        print(k, "median of lab1:")
        print(data[k]['lab1'].median())
        print(k, "variance by lab1:")
        print(data[k]['lab1'].std()**2)

        # plot the probability density function for each sensor type in lab 1
        plt.figure()
        pdf = (data[k]['lab1']).plot.density()
        plt.xlabel(k)
        title = k + ": Probability Density Function"
        plt.title(title)
        plt.savefig('images/'+k+'_PDF.png')

        print("\n")


    # finds the mean and variance of the time interval of sensor readings
    times = data["temperature"].index
    timeintervals = times[1:]-times[:-1]
    print("Mean of time intervals: ", timeintervals.mean().total_seconds())
    std = timeintervals.std().total_seconds()
    var = std**2
    print("Variance of time intervals:", var)

    # plot the probability density function fr the time interval of sensor readings
    timeintervalsseconds = timeintervals.total_seconds().to_series()
    timedata = timeintervalsseconds.to_frame();
    pdftime = timedata.plot.density()
    plt.xlabel("Time intervals (seconds)")
    plt.title("Time Intervals: Probability Density Function")

    plt.savefig('images/Time_Interval_PDF.png')

    officemean = data['temperature']['office'].mean();
    class1mean = data['temperature']['class1'].mean();
    lab1mean = data['temperature']['lab1'].mean();
    officestd = data['temperature']['office'].std();
    class1std = data['temperature']['class1'].std();
    lab1std = data['temperature']['lab1'].std();
    print("\n")
    print("office low ", officemean - 2*officestd)
    print("office high ", officemean + 2*officestd)
    print("class1 low ", class1mean - 2*class1std)
    print("class1 high ", class1mean + 2*class1std)
    print("lab1 low ", lab1mean - 2*lab1std)
    print("lab1 high ", lab1mean + 2*lab1std)


    plt.show()
