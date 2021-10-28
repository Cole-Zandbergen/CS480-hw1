####################################################
#   Code for CS480 homework1
#   Author: Cole Zandbergen
####################################################

import csv
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt, degrees
import datetime

#filepath = input("Enter the filepath for the folder containing your CSV files: ")
#get the user to enter the filepath

#for now, i'll just hardcode the filepath
filepath = "/Users/colezandbergen/Desktop/fall 2021/CS480/homework/hw1/code/data_raw"
outpath = "/Users/colezandbergen/Desktop/github/CS480-hw1"

ActivityChanges = open(filepath + '/activityChanges.csv', 'r')
ACC = open(filepath + '/sensoringData_acc.csv')
GPS = open(filepath + '/sensoringData_gps.csv')
Gyro = open(filepath + '/sensoringData_gyro.csv')
Magnetic = open(filepath + '/sensoringData_magn.csv')

##########
#	First, we need to find out if one or more suspects were within 100 meters of each other at any given time
##########

def haversine(lat1, lon1, lat2, lon2): #distance function, copied from stackoverflow

      R = 6372.8 # kilometers, total radius of earth --- i think

      dLat = radians(lat2 - lat1)
      dLon = radians(lon2 - lon1)
      lat1 = radians(lat1)
      lat2 = radians(lat2)

      a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
      c = 2*asin(sqrt(a))

      return R * c

def adjustLocation(start, end):
	l = [start[0] + end[0], start[1] + end[1]]
	return l

def findClose(suspects):
	
	for i in range(0, len(suspects)):
		for j in range(i+1, len(suspects)):
			for iTime in suspects[i].locationPlot:
				#print("checking i time " + iTime)
				for jTime in suspects[j].locationPlot:
					#print("checking j time " + jTime)
					diff = float(iTime) - float(jTime)
					if abs(diff) < 3600:
						if haversine(suspects[i].locationPlot.get(iTime)[0], suspects[i].locationPlot.get(iTime)[1], suspects[j].locationPlot.get(jTime)[0], suspects[j].locationPlot.get(jTime)[1]) < 0.1:
							print("Suspect " + suspects[i].name + " and " + suspects[j].name + " were close on " + str(datetime.datetime.fromtimestamp(float(iTime))))
					elif diff > 3600:
						break

#lets create a class to store suspects
class Suspect:
	def __init__(self, name, endingLocation, num):
		self.data = []
		self.name = name
		self.locationPlot = {}
		self.plotData = []
		self.currentLocation = endingLocation
		self.closePoints = {}
		self.closeids = []
		self.closeSuspects = []
		self.placeInList = num
		self.rawData = []

	def plotGPSData(self): #add a row of data to this suspect's list of data, it will need to be added in order of last timestamp first
		#we will assume that the data is in order from least to greatest timestamp, and add each piece of information to the front of the list
		'''self.data.insert(0, row)
		newLocation = [self.currentLocation[0] + float(row[3]), self.currentLocation[1] + float(row[4])]
		self.locationPlot[row[2]] = [adjustLocation(newLocation, self.endLocation)]
		self.currentLocation = newLocation'''
		#self.data.reverse() #first, reverse the data, since we must start from an ending location

		#NEW METHOD
		for row in reversed(self.data): #loop through the *reversed* list, since we must start from the ending location

			bearing = float(row[7])
			latinc = cos(radians(bearing)) * float(row[3])
			longinc = sin(radians(bearing)) * float(row[4])
			newLocation = [self.currentLocation[0] - latinc, self.currentLocation[1] - longinc]
			self.locationPlot[row[2]] = newLocation
			self.currentLocation = newLocation

			newRow = {'ID':"", 'time':"", 'lat':"", 'long':""}
			newRow['ID'] = self.name
			newRow['time'] = datetime.datetime.fromtimestamp(float(row[2]))
			newRow['lat'] = newLocation[0]
			newRow['long'] = newLocation[1]
			self.plotData.insert(0, newRow)


	def addData(self, row):
		self.data.append(row)
		#print("data added for " + str(self.name))
	
	def addTextLine(self, line):
		self.rawData.append(line)

	def findSuspectsAtSameTime(self, list):
		for s in list:
			if s.name != self.name:
				for p in s.locationPlot:
					hasBeenFound = False
					for t in self.locationPlot:
						if abs(float(p)-float(t)) < 2540 and not hasBeenFound: #if timestamps are within an hour of each other
							#hasBeenFound = True
							#self.closePoints[p] = [s.name, [s.locationPlot.get(p)]]
							#print("adding " + str(self.closePoints.get(p)) + " to list for " + str(self.name) + " at timestamp " + p)
							if(haversine(self.locationPlot.get(t)[0], self.locationPlot.get(t)[1], s.locationPlot.get(p)[0], s.locationPlot.get(p)[1])) <= 0.1:
								hasBeenFound = True
								#if the distance between those two points is less then 100 meters, or 0.1 kilometers
								self.closePoints[p] = [s.name, [s.locationPlot.get(p)]]
								print("adding " + str(self.closePoints.get(p)) + " to list for " + str(self.name) + " at timestamp " + p)
								#print("distance is " + str(haversine(self.locationPlot.get(t)[0], self.locationPlot.get(t)[1], s.locationPlot.get(p)[0], s.locationPlot.get(p)[1])))
								#rows.append([self.name, s.name, t, p, haversine(self.locationPlot.get(t)[0], self.locationPlot.get(t)[1], s.locationPlot.get(p)[0], s.locationPlot.get(p)[1])])
								newDict = {'Suspect':"", 'Close Suspect':"", 'Suspect Time':"", 'Close Suspect Time':"", 'Time Difference':"", 'Distance':""}
								newDict['Suspect'] = self.name
								newDict['Close Suspect'] = s.name
								newDict['Close Suspect Time'] = datetime.datetime.fromtimestamp(float(p))
								newDict['Distance'] = haversine(self.locationPlot.get(t)[0], self.locationPlot.get(t)[1], s.locationPlot.get(p)[0], s.locationPlot.get(p)[1])
								newDict['Suspect Time'] = datetime.datetime.fromtimestamp(float(t))
								newDict['Time Difference'] = abs(float(t) - float(p))
								self.closeSuspects.append(newDict)

def initializeSuspectObjects():
	#this will read the GPS file
	rows = []
	suspects = []

	reader = csv.reader(GPS)
	
	counter = 0
	for row in reader:
		inList = False #boolean to keep track of whether this suspect has already been added to the list
		suspect = None #initialize new suspect object
		for s in suspects:
			if s.name == row[1]:
				inList = True #set inlist to true if we don't need to create a new player
				suspect = s

		if not inList:
			suspect = Suspect(row[1], [43.33352346016208, -8.40940731683987], counter)
			suspects.append(suspect) #create new suspect and add him to our list
			counter += 1

		suspect.addData(row)

	return suspects

def plotSuspectGPSData(suspects):
	for s in suspects: #now get each suspect to create its location data dict
		s.plotGPSData()

#function to return a suspect from a list with the specified name
def getSuspectByName(name, suspects):
	for s in suspects:
		if(s.name == name):
			return s


suspects = initializeSuspectObjects()
plotSuspectGPSData(suspects)


#findClose(suspects)

'''with open(outpath+"/output.csv", 'w') as outfile:
	writer = csv.DictWriter(outfile, fieldnames=['Suspect', 'Close Suspect', 'Suspect Time', 'Close Suspect Time', 'Time Difference', 'Distance'])
	writer.writeheader()
	for s in suspects:
		writer.writerows(s.closeSuspects)'''

'''with open(outpath+"/suspectLocationPlot.csv", 'w') as outfile:
	w = csv.DictWriter(outfile, fieldnames=['ID', 'time', 'lat', 'long'])
	w.writeheader()
	for s in suspects:
		w.writerows(s.plotData)'''


###
# code to print the generated GPS plot from 18 and 12 to a csv file
###
'''with open(outpath+"/18and12.csv", 'w') as outfile:
	w = csv.DictWriter(outfile, fieldnames=['ID', 'time', 'lat', 'long'])
	w.writeheader()
	for s in suspects:
		if s.name == '18' or s.name == '12':
			w.writerows(s.plotData)'''