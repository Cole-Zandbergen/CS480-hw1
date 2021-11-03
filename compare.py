import main
import datetime

infile = main.outpath + "/18and12.csv"

suspects = main.initializeSuspectObjects()

s18 = main.getSuspectByName('18', suspects)
s12 = main.getSuspectByName('12', suspects)
s18.plotGPSData()
s12.plotGPSData()

for p in s12.plotData:
    for p1 in s18.plotData:
        if(abs(p['time'] - p1['time']) < datetime.timedelta(minutes=20)):
            distance = main.haversine(p['lat'], p['long'], p1['lat'], p1['long']) * 1000.0
            if(distance < 100):
                print("time for s12: " + str(p['time']) + "; location for s12: (" + str(p['lat']) + ", " + str(p['long']) + ")")
                print("time for s18: " + str(p1['time']) + "; location for s18: (" + str(p1['lat']) + ", " + str(p1['long']) + ")")
                print("distance between two points: " + str(distance) + " meters")