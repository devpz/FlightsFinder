import requests
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import json
import sys

def alter_price(price_type, flights):
	if price_type == "wdc":
		[flight.update({"priceType": "wdc"}) for flight in flights]
	else:
		[flight.update({"priceType": "regular"}) for flight in flights]
	return flights

headers = {
	'authority': 'be.wizzair.com',
	'accept': 'application/json, text/plain, */*',
	'origin': 'https://wizzair.com',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
	'content-type': 'application/json;charset=UTF-8',
	'sec-fetch-site': 'same-site',
	'sec-fetch-mode': 'cors',
	'referer': 'https://wizzair.com/en-gb/flights/timetable',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6'}


data = {"flightList":[{"departureStation":"WAW", 
					   "arrivalStation":"",
					   "from":"",
					   "to":""},
					  {"departureStation":"",
					   "arrivalStation":"WAW", 
					   "from":"",
					   "to":""}],"priceType":"","adultCount":1,"childCount":0,"infantCount":0}


destinations = ["ORY"]

data_list = []
base = datetime.today()

def save_response_text(response, filename):
    with open(filename, 'w') as file:
        file.write(response.text)
		
filename = 'server_response.txt'
		
        

for period in range(1):
	
	data["flightList"][0]["from"] = (base + timedelta(days = period * 42)).strftime("%Y-%m-%d")
	data["flightList"][1]["from"] = (base + timedelta(days = period * 42)).strftime("%Y-%m-%d")

	data["flightList"][0]["to"] = (base + timedelta(days = (period + 1) * 42)).strftime("%Y-%m-%d")
	data["flightList"][1]["to"] = (base + timedelta(days = (period + 1) * 42)).strftime("%Y-%m-%d")
	for price_type in ["regular", "wdc"]:
		data["priceType"] = price_type
		print(f"Downloading started with the following params for all destinations: {period}, {price_type}")
		for destination in tqdm(destinations):
			data["flightList"][0]["arrivalStation"] = destination
			data["flightList"][1]["departureStation"] = destination
			
			response = requests.post('https://be.wizzair.com/20.4.0/Api/search/timetable', headers=headers, data=json.dumps(data))
			if response.status_code == 200:
                
				save_response_text(response, filename)
				
				
				
			else:
				print("HTTP status: ", response.status_code)
				print("Something went wrong with this payload: ", data)

flat_list = [item for sublist in data_list for item in sublist]
df = pd.DataFrame(flat_list)




df.to_pickle("./wizzair_timetable_data.pkl")


