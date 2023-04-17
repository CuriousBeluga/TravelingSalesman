#CS 5007 HMWK 5
#Sean Tseng
#sltseng@wpi.edu

#Traveling Salesman Problem
#Import packages to be used
import pandas as pd
import random as rdm
import matplotlib.pyplot as plt
import math

#This implementation of the TSP with very basic greedy algorithm aka nearest neighbor
class TSP():

    #Find the distance between each of the cities to each other
    def find_distances(self):
        distance_List = {}
        for city1 in self.selected_cities:
            distance_List[city1] = {}
            for city2 in self.selected_cities:
                if city1 != city2:
                    distance_List[city1][city2] = self.distance(city1,city2)
        return distance_List


    #Function to calculate the distance between two cities using Haversine formula
    #Source https://www.igismap.com/haversine-formula-calculate-geographic-distance-earth/
    def distance(self,city1,city2):
        lat1, lng1 = self.cities[city1]['latitude'], self.cities[city1]['longitude']
        lat2, lng2 = self.cities[city2]['latitude'], self.cities[city2]['longitude']
        R = 6371  # Earth's radius in km
        phi1 = math.radians(lat1)       #convert latitude and longitude to radians
        phi2 = math.radians(lat2) 
        lam1 = math.radians(lng1)
        lam2 = math.radians(lng2)
        a = math.sin(math.radians(lat2-lat1)/ 2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(math.radians(lng2-lng1)/2)**2
        c = 2*math.atan2(math.sqrt(a),math.sqrt(1 - a))
        d = R*c
        return d

    def __init__(self):
        #Read the CSV file using pandas package
        df = pd.read_csv('uscities.csv')
        #Create random number to select cities
        rand_select = rdm.randint(4,30)       #Keep small for now to keep comp time low
        print(rand_select)
        self.selected_cities = rdm.sample(list(df['city']), rand_select)
        #Store state adress and coordinates of selected cities in dictionary
        self.cities = {}
        for index, row in df.iterrows():
            if row['city'] in self.selected_cities:
                self.cities[row['city']] = {'state': row['state_id'],
                                       'latitude': row['lat'],
                                       'longitude': row['lng']}
        #Check: print data to see if data read was successful
        #for city in self.cities:
            #print(f"{city},{self.cities[city]['state']} = Latitude: {self.cities[city]['latitude']}, Longitude: {self.cities[city]['longitude']}")

        #Find the distances between each of the cities
        self.distances = self.find_distances()

        #Create empty tour list
        self.tour = []
       
        #Tour function which generates the path using nearest neighbor greedy algorithm
        #nearest neighbor is not the most accurate, but has a lean time to calculate a solution that is close to accurate
    def tour_func(self):
        #Create path of selected cities using the nearest neighbor algorithm
        current_city = self.selected_cities[0]
        #store remaining cities in set, which cannot contain duplicate entries
        remain_cities = set(self.selected_cities[1:])
        self.tour.append(current_city)
        #while loop executes if cities still remain on list
        while remain_cities:
            #find the nearest neighbor by using min function between remainder cities and current city)
            nearest_city = min(remain_cities, key=lambda city: self.distances[current_city][city])
            remain_cities.remove(nearest_city)
            self.tour.append(nearest_city)
            current_city = nearest_city
        #append first city to end to complete travel
        self.tour.append(self.selected_cities[0])
      
        #Find the length of the tour
    def tLength(self):    
        len_tour = 0
        for i in range(len(self.tour)-1):
            city1, city2 = self.tour[i], self.tour[i+1]
            len_tour += self.distances[city1][city2]
        return len_tour

    #Str and total_plot are meant for the user to call as methods
    def __str__(self):
        #Call to tour function to make the tour and a call to the tour length function for total distance
        tour = self.tour_func()
        tour_length = self.tLength()
        #empty string for storing tour message
        t_string =[]

        #Print tour and tour length
        for i in range(len(self.tour)):
            #First Stop
            if i ==0:
                city = self.tour[i]
                state = self.cities[city]['state']
                t_string.append(f'\nStarting city: {city}, {state}')
            #Final stop
            elif i == len(self.tour)-1:
                city = self.tour[i]
                state = self.cities[city]['state']
                t_string.append(f'\nFinal city: {city}, {state}')
            #All other stops
            else:
                city = self.tour[i]
                state = self.cities[city]['state']
                t_string.append(f'\nStop #{i}: {city}, {state}')
         
        return '\n'.join(t_string) + f'\nTotal tour length: {tour_length} km'

    def total_plot(self):
        #Longtitude and latitude for graph plot
        tour_latitudes = [self.cities[city]['latitude'] for city in self.tour]
        tour_longitudes = [self.cities[city]['longitude'] for city in self.tour]

        #Plot tour
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df['lng'], df['lat'], s=0.5, alpha=0.2)
        ax.plot(tour_longitudes, tour_latitudes, '-o', color='red', markersize=5)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title(f'Tour of {len(selected_cities)} Random US cities')
        plt.show()

#Testing the TSP class
Tour_1 = TSP()
Tour_2 = TSP()

print(Tour_1)
print(Tour_2)

