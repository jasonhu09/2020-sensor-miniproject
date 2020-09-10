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

    print(type(temperature))
    print(type(data))
    #print(data['temperature']['office'].values())
    newdict = data['temperature']['office'];
    #print(newdict.values)
    #print(data['temperature'].index)

    #timeintervals = data['temperature'].index.to_pytimedelta()
    #print(timeintervals)
    #times = data['temperature'].index
    #print(type(times))
    #time1 = times[:-1]
    #time2 = times[1:]
    #print(times, "\n")
    #print(time1,"\n")
    #print(time2,"\n")
    #print(times.size)
    #print(time1.size)
    #print(time2.size)

    #timeintervals = time2-time1;
    #print(timeintervals);
    #print(timeintervals.size)
    #timeintervals = [time2 - time1 for time1, time2 in zip(times[:-1], times[1:])]
    #print(timeintervals)

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)




    #print(data)
    for k in data:
        # data[k].plot()
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")

        print(k)
        print(data[k].median())
        print(data[k].std()**2)
        pdf = data[k].plot.density()



        print("\n")

    plt.show()

    times = data["temperature"].index
    print("times:\n", times);
    timeintervals = times[1:]-times[:-1]
    print(type(timeintervals))
    print(type(timeintervals.total_seconds()))
    print("mean: ", timeintervals.mean().total_seconds())
    #print(timeintervals.std().nanoseconds)
    std = timeintervals.std().total_seconds()
    var = std**2
    #print(float(std.seconds))
    print("var:", var)


    print(timeintervals);
    print(timeintervals.total_seconds())
    print(timeintervals.total_seconds().to_series())
    print(type(timeintervals.total_seconds().to_series()))

    timeintervalsseconds = timeintervals.total_seconds().to_series()


    print(type(timeintervalsseconds.to_frame()))
    timedata = timeintervalsseconds.to_frame(index = False);
    timedata.plot.density()
    plt.xlabel("Time intervals (seconds)")
    plt.ylabel("Probability")
    plt.title("PDF plot of the time intervals")
    plt.savefig("PDF_time_intervals.png")
    #print(timeintervals.to_frame()[0][1].total_seconds())
    #timeintervals.to_frame().plot.hist()
    #pdf2 = timeintervals.to_frame().plot.density()

    #plt.show()
    #pdf.show()
