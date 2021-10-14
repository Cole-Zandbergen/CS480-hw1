####################################################
#   Code for CS480 homework1
#   Author: Cole Zandbergen
####################################################

filepath = input("Enter the filepath for the folder containing your CSV files: ")
#get the user to enter the filepath

ActivityChanges = open(filepath + '/activityChanges.csv', 'r')
ACC = open(filepath + '/sensoringData_acc.csv')
GPS = open(filepath + '/sensoringData_gps.csv')
Gyro = open(filepath + '/sensoringData_gyro.csv')
Magnetic = open(filepath + '/sensoringData_magn.csv')
