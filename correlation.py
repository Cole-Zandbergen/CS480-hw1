import main
import pandas as pd
import numpy as np

print("reading files...")
#ACtable = pd.read_csv(main.ActivityChanges)
GPStable = pd.read_csv(main.GPS)
GPSLocationTable = pd.read_csv("suspectLocationPlot.csv")
#ACCtable = pd.read_csv(main.ACC)
#GyroTable = pd.read_csv(main.Gyro)
#Mtable = pd.read_csv(main.Magnetic)

print("files read...")

def getSuspects(df):
    return df.groupby(df.username)

def get_corrs(df):
    col_correlations = df.corr()
    col_correlations.loc[:, :] = np.tril(col_correlations, k=-1)
    cor_pairs = col_correlations.stack()
    return cor_pairs.to_dict()

susList = getSuspects(GPStable)
susListLocation = GPSLocationTable.groupby(GPSLocationTable.ID)
#print(susList.get_group(11))
#corrList = []

#correlations = get_corrs(table)
print("getting correlations")

#ACcor = get_corrs(ACtable)
GPScor = get_corrs(GPStable)
GPSLocationCorr = get_corrs(GPSLocationTable)
#ACCcor = get_corrs(ACCtable)
#GyroCor = get_corrs(GyroTable)
#MagCor = get_corrs(Mtable)

'''for s in susList:
    corrList.append(get_corrs(s))'''

def significant(n):
    if abs(n) > 0.3:
        return True
    else:
        return False


'''for i in sorted(correlations, key=correlations.get, reverse=True):
    print("Correlation between: " + str(i) + " is " + str(correlations.get(i)))'''

'''for i in sorted(c1, key=c1.get, reverse=True):
    print("Correlation between: " + str(i) + " is " + str(c1.get(i)))'''


print("printing output...")

with open("correlations.txt", 'w') as outfile:
    outfile.write("Correlations for the Activity Changes data: \n")
    '''for i in sorted(ACcor, key=ACcor.get, reverse=True):
        if significant(ACcor.get(i)):
            outfile.write("Correlation between " + str(i) + " is " + str(ACcor.get(i)) + "\n")'''

    outfile.write("\n\nCorrelations for the GPS data: \n")
        
    for i in sorted(GPScor, key=GPScor.get, reverse=True):
        if significant(GPScor.get(i)):
            outfile.write("Correlation between " + str(i) + " is " + str(GPScor.get(i)) + "\n")

    '''outfile.write("\n\nCorrelations for the ACC data: \n")

    for i in sorted(ACCcor, key=ACCcor.get, reverse=True):
        if significant(ACCcor.get(i)):
            outfile.write("Correlation between " + str(i) + " is " + str(ACCcor.get(i)) + "\n")

    outfile.write("\n\nCorrelations for the Gyro data: \n")

    for i in sorted(GyroCor, key=GyroCor.get, reverse=True):
        if significant(GyroCor.get(i)):
            outfile.write("Correlation between " + str(i) + " is " + str(GyroCor.get(i)) + "\n")

    outfile.write("\n\nCorrelations for the magnetic sensor data: \n")

    for i in sorted(MagCor, key=MagCor.get, reverse=True):
        if significant(MagCor.get(i)):
            outfile.write("Correlation between " + str(i) + " is " + str(MagCor.get(i)) + "\n")'''


    for s in main.suspects:
        outfile.write("\n\nFor suspect number " + s.name + ":\n")
        corrs = get_corrs(susList.get_group(int(s.name)))
        corrs1 = get_corrs(susListLocation.get_group(int(s.name)))
        for i in sorted(corrs, key=corrs.get, reverse=True):
            if significant(corrs.get(i)):
                outfile.write("Correlation between " + str(i) + " is " + str(corrs.get(i)) + "\n")
        outfile.write("\nFor the user's table with actual location plot points:\n")
        for i in sorted(corrs1, key=corrs1.get, reverse=True):
            if significant(corrs1.get(i)):
                outfile.write("Correlation between " + str(i) + " is " + str(corrs1.get(i)) + "\n")

    
            

print("Program finished!")