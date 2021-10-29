import main
import csv
from matplotlib import pyplot
#import mpl_toolkits.mplot3d

suspects = main.initializeSuspectObjects()

suspect18 = main.getSuspectByName('18', suspects)
suspect12 = main.getSuspectByName('12', suspects)

with open(main.outpath+"/18and12fulldata.csv", 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id','username','timestamp','gps_lat_increment','gps_long_increment','gps_alt_increment','gps_speed','gps_bearing','gps_accuracy','activity_id','activity'])
    writer.writerows(suspect18.data)
    writer.writerows(suspect12.data)
print("done!")


#now, plot the GPS data from the suspects
suspect18.plotGPSData()
suspect12.plotGPSData()

lat18 = []
long18 = []
time18 = []
for l in suspect18.plotData:
    lat18.append(l['lat'])
    long18.append(l['long'])
    time18.append(l['time'])

lat12 = []
long12 = []
time12 = []
for l in suspect12.plotData:
    lat12.append(l['lat'])
    long12.append(l['long'])
    time12.append(l['time'])

print("The amount of data for 18 is " + str(len(lat18)))
print("The amound of data for 12 is " + str(len(lat12)))

#PLOT THE DATA:
pyplot.plot(lat18, long18, color="red")
pyplot.plot(lat12, long12, color="blue")
pyplot.xlabel("latitude")
pyplot.ylabel("longitude")

pyplot.show()

'''f = pyplot.figure()
ax = f.add_subplot(111, projection = '3d')
ax.set_xlabel('latitude')
ax.set_ylabel('longitude')
ax.set_zlabel('time')

ax.plot(lat12, long12, time12)
ax.plot(lat18, long18, time18)
pyplot.show()'''