####################################################
#   Code for CS480 homework1
#   Author: Cole Zandbergen
####################################################

import csv
import matplotlib.pyplot as plt

filepath = input("Enter the filepath for the folder containing your CSV files: ")
#get the user to enter the filepath

ActivityChanges = open(filepath + '/activityChanges.csv', 'r')
ACC = open(filepath + '/sensoringData_acc.csv')
GPS = open(filepath + '/sensoringData_gps.csv')
Gyro = open(filepath + '/sensoringData_gyro.csv')
Magnetic = open(filepath + '/sensoringData_magn.csv')

##########
#	First, we need to find out if one or more suspects were within 100 meters of each other at any given time
##########

def adjustLocation(start, end):
	l = [start[0] + end[0], start[1] + end[1]]
	return l

#lets create a class to store suspects
class Suspect:
	def __init__(self, name, endingLocation):
		self.data = []
		self.name = name
		self.locationPlot = {}
		self.currentLocation = endingLocation

	def plotGPSData(self): #add a row of data to this suspect's list of data, it will need to be added in order of last timestamp first
		#we will assume that the data is in order from least to greatest timestamp, and add each piece of information to the front of the list
		'''self.data.insert(0, row)
		newLocation = [self.currentLocation[0] + float(row[3]), self.currentLocation[1] + float(row[4])]
		self.locationPlot[row[2]] = [adjustLocation(newLocation, self.endLocation)]
		self.currentLocation = newLocation'''
		#self.data.reverse() #first, reverse the data, since we must start from an ending location


		for row in reversed(self.data): #loop through the *reversed* list, since we must start from the ending location
			newLocation = [self.currentLocation[0] - float(row[3]), self.currentLocation[1] - float(row[4])]
			self.locationPlot[row[2]] = newLocation
			self.currentLocation = newLocation

	def addData(self, row):
		self.data.append(row)
		#print("data added for " + str(self.name))


#this will read the GPS file
rows = []

suspects = []

reader = csv.reader(GPS)
header = next(reader)
for row in reader:
	inList = False #boolean to keep track of whether this suspect has already been added to the list
	suspect = None #initialize new suspect object
	for s in suspects:
		if s.name == row[1]:
			inList = True #set inlist to true if we don't need to create a new player
			suspect = s

	if not inList:
		suspect = Suspect(row[1], [43.33352346016208, -8.40940731683987])
		suspects.append(suspect) #create new suspect and add him to our list

	suspect.addData(row)

for s in suspects: #now get each suspect to create its location data dict
	s.plotGPSData()

for i in suspects[0].locationPlot:
	#print(i)
	l = []
	l.append(i)
	for n in l:
		print(suspects[0].locationPlot.get(n))

GPS.close()