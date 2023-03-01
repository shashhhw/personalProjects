'''
Authors: Shashwat Maharjan and Megan Mearnic
2023 Reimagine Hackathon Team: ChipMaps

This code utilizes the Google Map API to find directions between
locations. This code then utilizes the provided locations by 
Google maps to then personalize the direction recommendations so
that CMU buildings can be used as references to nagivate campus.

An output ".txt" file is attached to the submission link to observe the output.
'''

import os
import googlemaps
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
import pickle

# Define a function to remove HTML tags
def remove_HTML_tags(string):
     
    # Return string after removing tags
    return re.compile(r'<[^>]+>').sub('', string)

def main():

    # Clear screen
    os.system("clear")

    print("\nRunning navigatingCMU.py\n")

    # Initialize google maps from Google Maps API
    API_KEY = "AIzaSyCQf7SWDsM3Xv5QlFlGwnglY4t-VtxuUJs"
    # API_KEY = "AIzaSyCBmXf_o8VL9gYrpAGO58lGiCy2BlTjgn8"
    gmaps = googlemaps.Client(key=API_KEY)

    # Read ".xlsx" file for all CMU locations
    excelFilePath = "/Users/mahar1s/Documents/VSCodeProjects/hackathonProject/cmuLocations.xlsx"
    allLocations = pd.read_excel(excelFilePath, sheet_name="Sheet1")

    # Create an empty dictionary to store values for the application
    backendFileInformation = {}

    # Define origin addresses
    userOrigin = "Engineering Building"
    backendFileInformation["Origin"] = userOrigin
    # userOrigin = "Bovee University Center"

    originLatitude  = allLocations[allLocations["Location"] == userOrigin]["Latitude"]
    originLongitude  = allLocations[allLocations["Location"] == userOrigin]["Longitude"]

    originGeocode = gmaps.reverse_geocode((originLatitude, originLongitude))
    originAddress = originGeocode[0]["formatted_address"]

    # Define destination addresses
    userDestination = "Northwest Apartments"
    backendFileInformation["Destination"] = userDestination
    # userDestination = "Education and Human Services"

    destinationLatitude  = allLocations[allLocations["Location"] == userDestination]["Latitude"]
    destinationLongitude  = allLocations[allLocations["Location"] == userDestination]["Longitude"]

    destinationGeocode = gmaps.reverse_geocode((destinationLatitude, destinationLongitude))
    destinationAddress = destinationGeocode[0]["formatted_address"]

    distanceInformation = gmaps.distance_matrix(origins=originAddress, destinations=destinationAddress, mode="walking", departure_time=datetime.now() + timedelta(minutes=0.1))
    originDestinationDistance = int(distanceInformation["rows"][0]["elements"][0]["distance"]["value"]) # in m
    originDestinationTime = int(distanceInformation["rows"][0]["elements"][0]["duration"]["value"]) # in min

    print("You are at %s." %(originAddress))
    print("You will travel %s m for %s min to reach %s." %(originDestinationDistance, originDestinationTime, destinationAddress))

    directionsResult = gmaps.directions(originAddress, destinationAddress, mode="walking", arrival_time=datetime.now() + timedelta(minutes=0.1))
    directions = directionsResult[0]["legs"][0]["steps"]

    notDroppedLocations = allLocations
    locationToBeDropped = allLocations[(allLocations["Location"] == userOrigin) | (allLocations["Location"] == userDestination)].index
    notDroppedLocations.drop(locationToBeDropped, inplace=True)

    closestDistanceList = np.zeros((len(notDroppedLocations)))

    locationsRecorded = []
    locationsRecorded.append(userOrigin)

    instructionDict = {"Step " + str(i):{} for i in range(1, len(directions)+1)}
    instructionSteps = list(instructionDict.keys())
    backendFileInformation["Instructions"] = instructionDict

    pathDict = {"Path " + str(i):{} for i in range(1, len(directions)+1)}
    pathSteps = list(pathDict.keys())
    backendFileInformation["Paths"] = pathDict


    for stepNumber in range(len((directions))):

        time = directions[stepNumber]["duration"]["text"]
        distance = directions[stepNumber]["distance"]["text"]

        startLocationLatitude = directions[stepNumber]["start_location"]["lat"]
        startLocationLongitude = directions[stepNumber]["start_location"]["lng"]

        endLocationLatitude = directions[stepNumber]["end_location"]["lat"]
        endLocationLongitude = directions[stepNumber]["end_location"]["lng"]

        endLocationGeocode = gmaps.reverse_geocode((endLocationLatitude, endLocationLongitude))
        endLocationAddress = endLocationGeocode[0]["formatted_address"]

        backendFileInformation["Paths"][pathSteps[stepNumber]]["Intial Position"] = [startLocationLatitude, startLocationLongitude]
        backendFileInformation["Paths"][pathSteps[stepNumber]]["Final Position"] = [endLocationLatitude, endLocationLongitude]

        for nCMULocation in range(len(notDroppedLocations)):

            closestLocationLatitude = notDroppedLocations.iloc[nCMULocation]["Latitude"]
            closestLocationLongitude = notDroppedLocations.iloc[nCMULocation]["Longitude"]

            closestLocationGeocode = gmaps.reverse_geocode((closestLocationLatitude, closestLocationLongitude))
            closestAddress = closestLocationGeocode[0]["formatted_address"]

            distanceBetweenEndClosest = gmaps.distance_matrix(origins=endLocationAddress, destinations=closestAddress, mode="walking")#, departure_time=datetime.now() + timedelta(minutes=0.1))
            closestDistanceList[nCMULocation] = distanceBetweenEndClosest["rows"][0]["elements"][0]["duration"]["value"]
        
        closestDistanceIndex = np.where(closestDistanceList == np.min(closestDistanceList))
        closestDistanceLocation = closestDistanceIndex[0][0]

        if stepNumber == 0:

            instructions = remove_HTML_tags(directions[stepNumber]["html_instructions"])
            print("\nStep %d: %s from the %s for %s. You should be heading towards %s." %(stepNumber+1, instructions, userOrigin, time, notDroppedLocations.iloc[closestDistanceLocation]["Location"]))

            backendFileInformation["Instructions"][instructionSteps[stepNumber]] = instructions + " from the " + userOrigin + " for " + time + ". You should be heading towards " + notDroppedLocations.iloc[closestDistanceLocation]["Location"] + "."

            prevLocation = notDroppedLocations.iloc[closestDistanceLocation]["Location"]
            locationsRecorded.append(prevLocation)

        elif stepNumber == len(directions)-1:

            instructions = directions[stepNumber]["html_instructions"]
            splitInstruction = instructions.split("</b>")

            newInstruction = []

            for nLen in range(len(splitInstruction)):
                newInstruction.append(remove_HTML_tags(splitInstruction[nLen]))

            print("Step %d: %s and walk %s for %s to reach %s." %(stepNumber+1, newInstruction[0], distance, time, userDestination))

            backendFileInformation["Instructions"][instructionSteps[stepNumber]] = newInstruction[0] + " and walk " + distance + " for " + time + " to reach " + userDestination + "."
        
        else:

            instructions = remove_HTML_tags(directions[stepNumber]["html_instructions"])

            if notDroppedLocations.iloc[closestDistanceLocation]["Location"] != prevLocation:
                print("Step %d: %s and walk %s for %s. You should be heading towards %s." %(stepNumber+1, instructions, distance, time, notDroppedLocations.iloc[closestDistanceLocation]["Location"]))
                prevLocation = notDroppedLocations.iloc[closestDistanceLocation]["Location"]
                locationsRecorded.append(prevLocation)

                backendFileInformation["Instructions"][instructionSteps[stepNumber]] = instructions + " and walk " + distance + " for " + time + ". You should be heading towards " + notDroppedLocations.iloc[closestDistanceLocation]["Location"] + "."

            else:
                
                locationsRecorded.append(prevLocation)
                print("Step %d: %s and walk %s for about %s." %(stepNumber+1, instructions, distance, time))

                backendFileInformation["Instructions"][instructionSteps[stepNumber]] = instructions + " and walk " + distance + " for about " + time + "."

    locationsRecorded.append(userDestination)

    # # Remove repeated locations
    locationsToBeShown = []
    [locationsToBeShown.append(locations) for locations in locationsRecorded if locations not in locationsToBeShown]

    backendFileInformation["Path Locations"] = locationsToBeShown

    with open('backend_file_information.pickle', 'wb') as handle:
        pickle.dump(backendFileInformation, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()