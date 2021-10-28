import main
import csv

suspects = main.initializeSuspectObjects()
print("Done initializing")

suspect18 = main.getSuspectByName('18')
suspect12 = main.getSuspectByName('12')

with open(main.outpath+"/18and12fulldata.csv", 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(suspect18.data)
    writer.writerows(suspect12.data)
print("done!")
