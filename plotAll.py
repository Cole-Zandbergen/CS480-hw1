from matplotlib import pyplot
import pandas as pd
#import matplotlib as plt
import main

map = pd.read_csv("suspectLocationPlot.csv")

suspectIDs = []
suspects = []


for i in map['ID']:
    if i not in suspectIDs:
        suspects.append(map[map['ID'] == i])
        suspectIDs.append(i)

for s in suspects:
    pyplot.plot(s['lat'], s['long'])


pyplot.xlabel("latitude")
pyplot.ylabel("longitude")

pyplot.show()