from .data_layer.load_csv import *
import json
import copy
from array import array


def Reverse_String(dict):

	payload = dict["payload_bus"]

	payload = str(payload[::-1])

	payload = payload.replace("'", '"')

	return payload

def Get_Top_5_Countries_Deaths():
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	country_deaths = 0.0
	payload = []
	tmp_list = []
	death_dict = {}
	state_max = 0.0

	for country_key, country_obj in tmp_countries_list.items():
		country_deaths = 0.0	
		for state_key, state_obj in country_obj.states.items():
			death_list = [] # deaths list per state
			for date_obj in state_obj.dates.values():
				tmp_list = date_obj.deaths
				#date_obj.deaths returns a list of strings containing all the deaths
				#then going to use this for loop convert that to a float to use the max
				for line in tmp_list.splitlines(): 
					#splits the in the tmp_list to a float 
				 	death_list.append(float(line))
				#at the end of the conversion you now have a list of float values for the state.dates
			state_max = max(death_list)	#using the max of the list of float for states
			country_deaths += state_max 

			
		death_dict[country_key] = country_deaths
	
	# TODO: store death dict somewhere so we do not have to find and sort every time
	# sort death dict so we can get top n countries by index
	death_dict = dict(sorted(death_dict.items(), key=lambda item: item[1], reverse=True)) 
	death_dict_keys = death_dict.keys()
	top_five_keys = list(death_dict_keys)[:5]
	death_dict_values = death_dict.values()
	top_five_values = list(death_dict_values)[:5]
	
	for i in range(0, 5):
		payload.append(
			{
			"Country":top_five_keys[i],
			"Deaths":top_five_values[i]
			}
		)

	print(payload)

def Get_Top_5_States_Cases(stateFilter):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	TotalArray = []
	total_deaths = 0.0
	finalTotal = []

	for country_key, country_obj in tmp_countries_list.items():
		if stateFilter in country_obj.states:
			for date_key, date_obj in country_obj.states[stateFilter].dates.items():
					total_deaths += float((tmp_countries_list[country_key].states[stateFilter].dates[date_key].reprJSON()["Confirmed"]))
					
		TotalArray.append(total_deaths)
	for x in range(5):
		finalTotal.append(max(TotalArray))
		TotalArray.remove(max(TotalArray))

	# tmp_list = []
	# death_list = []
	# death_dict = {}
	# for country_key, country_obj in tmp_countries_list.items():
	# 	for state_key, state_obj in country_obj.states.items():
	# 		for date_obj in state_obj.dates.values():
	# 			tmp_list = date_obj.deaths
	# 			for item in tmp_list.splitlines():
	# 				# if state_key == "California":
	# 				# 	ca_list.append(float(item))
	 			
	# 			 	death_list.append(float(item))
						
	# 		death_dict[country_key] = max(death_list)
	# 	death_list = []			

	print("States_Confirmed")
	print(finalTotal)

def Get_Top_5_States_Deaths(stateFilter):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	TotalArray = []
	total_deaths = 0.0
	finalTotal = []

	for country_key, country_obj in tmp_countries_list.items():
		if stateFilter in country_obj.states:
			for date_key, date_obj in country_obj.states[stateFilter].dates.items():
					total_deaths += float((tmp_countries_list[country_key].states[stateFilter].dates[date_key].reprJSON()["Deaths"]))
					
		TotalArray.append(total_deaths)
	for x in range(5):
		finalTotal.append(max(TotalArray))
		TotalArray.remove(max(TotalArray))

	print(finalTotal)
	
#left as the same in case we need to go back to this version
def Get_Top_5_States_Recovered(stateFilter):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	TotalArray = {}
	total_deaths = 0.0

	for country_key, country_obj in tmp_countries_list.items():
		if stateFilter in country_obj.states:
			for date_key, date_obj in country_obj.states[stateFilter].dates.items():
					total_deaths += float((tmp_countries_list[country_key].states[stateFilter].dates[date_key].reprJSON()["Recovered"]))
					
		TotalArray[country_key] = total_deaths

	print(max(TotalArray.values()))

#def Copy_Csv(self, pathOfOriginal):
	
#Backup CSV
def Backup_Csv(path):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()

	
		#print(tmp_countries_list["US"])

	SNo = ""
	LastUpdate = ""
	csv_country = ""
	csv_state = ""
	date = ""
	confirmed = ""
	deaths = ""
	recovered = ""
	with open(path, "w") as outfile:
		for countryKey, country in tmp_countries_list.items():
			csv_country = countryKey
			for stateKey, state in country.states.items():
				csv_state = stateKey
				for dates in state.dates.values():
					date = dates.date
					confirmed = dates.confirmed
					deaths = dates.deaths
					recovered = dates.recovered
					tmp_join = [SNo,date, csv_state,csv_country, date, confirmed, deaths, recovered]
					tmp_string = ",".join(tmp_join)
					tmp_string += "\n"
					outfile.write(tmp_string)



# SNo,ObservationDate,Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered
#Create(Country: USA, State: California, Confirmed : 0, Deaths: 0, Recovered: 0, Date: 9/11/2021)
def Create_Csv(country, state, type, date, amount):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	#if country is not in the tmp list
	#then we can just append to the dictionary becasuse that country doesn't exist
	#else it exists
	#then use that country as a key and append to that 

	#this checks if the country is in the country list dictionary
	# if country in tmp_countries_list:
		#date_obj is a date object that will be added to the country list
		#Since function only takes in specified input then we have to check
		#which type it is. After entering specified amount for type then
		#make the other 2 types default 0
	if date in tmp_countries_list[country].states[state].dates:

		print("Create Exist. Go To Edit Instead.")
	else: 
		
		if type == "Deaths":
			date_obj = Date(date,"0", str(amount), "0") 
		elif type == "Confirmed":
			date_obj = Date(date,str(amount), "0", "0") 
		elif type == "Recovered":
			#then make a date object to add to the country object
			date_obj = Date( date,"0", "0", str(amount))
			#sets country object dates to the date object
		tmp_countries_list[country].states[state].dates[date] = date_obj
			#finally add the country object to the countries list 
			#based on the country parameter from user 
		

	# else:
	# 	#the country doesn't exist  so need to make a country object
	# 	country_obj = Country(country)
	# 	if type == "Deaths":
	# 		date_obj = Date(date,"0", str(amount), "0") 
	# 	elif type == "Confirmed":
	# 		date_obj = Date(date,str(amount), "0", "0") 
	# 	elif type == "Recovered":
	# 		#then make a date object to add to the country object
	# 		date_obj = Date( date,"0", "0", str(amount))
	# 		#sets country object dates to the date object
	# 	country_obj.states[state].dates[date] = date_obj
	# 		#finally add the country object to the countries list 
	# 		#based on the country parameter from user 
	# 	tmp_countries_list[country] = country_obj
	
	#back in the load_csv.py 
	#will set the countries_data to tmp_countries_list so we can use the updated data 
	#print(tmp_countries_list[country].states[state])
	data_layer.set_countries(tmp_countries_list)

#only update the confirmed, deaths, or recovered cases
def Update_Csv(country, state, type, date, value):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	if country in tmp_countries_list:
		if state in tmp_countries_list[country].states:
			if date in tmp_countries_list[country].states[state].dates:
				if type == "Deaths":
					#print(tmp_countries_list[country].states[state].dates[date].reprJSON()[type])
					date_obj = Date( date, tmp_countries_list[country].states[state].dates[date].reprJSON()["Confirmed"], 
					str(value), tmp_countries_list[country].states[state].dates[date].reprJSON()["Recovered"]) 
					tmp_countries_list[country].states[state].dates[date] = date_obj
					print("Edit Deaths")
					#print(tmp_countries_list[country].states[state].dates[date].reprJSON()[type])
				elif type == "Recovered":
					date_obj = Date( date, tmp_countries_list[country].states[state].dates[date].reprJSON()["Confirmed"], 
					str(value), tmp_countries_list[country].states[state].dates[date].reprJSON()["Deaths"]) 
					tmp_countries_list[country].states[state].dates[date] = date_obj
					print("Edit Recovered")
				elif type == "Confirmed":			
					date_obj = Date( date, tmp_countries_list[country].states[state].dates[date].reprJSON()["Deaths"], 
					str(value), tmp_countries_list[country].states[state].dates[date].reprJSON()["Recovered"]) 
					tmp_countries_list[country].states[state].dates[date] = date_obj
					print("Edit Confirmed")
				else:
					print("Update doesnt work")
			else:
				print("Update couldn't find date")
	data_layer.set_countries(tmp_countries_list)

#type doesn't matter because you're deleting the whole row of values 
#i.e for 01/20/2020 you would delete the whole row
def Delete_Csv(country, state, date):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()

	#this checks if the country is in the country list dictionary
	#for key in tmp_countries_list:
	if country in tmp_countries_list:
		if state in tmp_countries_list[country].states:
			if date in tmp_countries_list[country].states[state].dates:
				#print(tmp_countries_list[country].states[state].dates[date])
				del tmp_countries_list[country].states[state].dates[date]
				#print(tmp_countries_list[country].states[state].dates[date])
				#print(tmp_countries_list)
		else:
			print("State no exist")
	else:
		print("Doesn't exist")

def Get_Filtered_Data(countryFilter, stateFilter, typeFilter, dateFilter):

	# putting payload into array so we can iterate thru and put into table?
	# list of jsons/dicts
	payload = []

	# importing the data layer object so we can use the functions within the method
	from .urls import data_layer

	countries_list = data_layer.get_countries()

	# TODO: none of these account for the dates dictionary inside country!
	# may need to include those later depending on if they contain useful data

	# TODO: might change format of load_csv later to fit a universal json format
	# NOTE: we can make a dynamic table that will change its value based on the json keys

	# NOTE: Aiming for a json format like this
	# {
	#   Country: "Japan"
	#   Date: "09/28/2020"
	#   State: "Tokyo"
	#   Types: {
	#   	Confirmed: "25345.0"
	#   	Deaths: "406.0"
	#   	Recovered: "22647.0"
	# 	}
	# }

	# this accounts for when country is empty or not empty, doesnt matter
	# when no fields are empty
	# return a json of of specific date of a state
	if countryFilter != "" and dateFilter != "" and stateFilter != "":
		if dateFilter in countries_list[countryFilter].states[stateFilter].dates:
			# just return the whole JSON instead of a specific case, let the front end pick which type of case
			payload.append(
				{
					"Country": countryFilter,
					"State": stateFilter,
					"Date": dateFilter,
					# maybe for larger objects like country and state we could use the total cases instead of per date
					"Types": countries_list[countryFilter]
					.states[stateFilter]
					.dates[dateFilter]
					.reprJSON(),
				}
			)
			# print("at country, date, state filled")

	# when country is empty
	# return data for that state and date
	elif countryFilter == "" and stateFilter != "" and dateFilter != "":
		for country_key, country_obj in countries_list.items():
			if stateFilter in country_obj.states:
				# checking if the date is a key within the state's dates dictionary
				if dateFilter in country_obj.states[stateFilter].dates:
					# just return the whole JSON instead of a specific case, let the front end pick which type of case
					payload.append(
						{
							"Country": country_key,  # <- these change
							"State": stateFilter,  # <- these change
							"Date": dateFilter,  # <- when var is given, this will always be the same so you can just slap it there
							"Types": country_obj.states[stateFilter].dates[dateFilter].reprJSON(),
						}
					)

	# when date field is empty
	# in this case, return all dates for a state
	elif countryFilter != "" and stateFilter != "" and dateFilter == "":
		# need date_key bc date filter is empty
		for date_key, date_obj in (
			countries_list[countryFilter].states[stateFilter].dates.items()
		):
			# adding to payload list
			payload.append(
				{
					# we already know the country since every state obj has a country name member within it
					"Country": countries_list[countryFilter].states[stateFilter].country_name,
					"State": stateFilter,
					"Date": date_key,
					"Types": date_obj.reprJSON(),
				}
			)

	# when country and date are empty
	# in this case, return all the dates of that state
	elif countryFilter == "" and stateFilter != "" and dateFilter == "":
		for country_key, country_obj in countries_list.items():
			if stateFilter in country_obj.states:
				for date_key, date_obj in country_obj.states[stateFilter].dates.items():
					# just return the whole JSON instead of a specific case, let the front end pick which type of case
					payload.append(
						{
							"Country": country_key,  # <- these change
							"State": stateFilter,  # <- these change
							"Date": date_key,  # <- when var is given, this will always be the same so you can just slap it there
							"Types": country_obj.states[stateFilter].dates[date_key].reprJSON(),
						}
					)

	# when state and date field is empty(basically all country data) TODO: maybe include country.dates
	# in this case, return all states and dates
	elif countryFilter != "" and stateFilter == "" and dateFilter == "":
		for state_key, state_obj in countries_list[countryFilter].states.items():
			for date_key, date_obj in state_obj.dates.items():
				if date_key in state_obj.dates:  # .dates returns a dictonary
					payload.append(
						{
							"Country": countryFilter,
							"State": state_key,
							"Date": date_key,
							"Types": date_obj.reprJSON(),
						}
					)

	# when state is empty
	# in this case, return all states, but only use the date given
	elif countryFilter != "" and stateFilter == "" and dateFilter != "":
		for state_key, state_obj in countries_list[countryFilter].states.items():
			# checking if the date is a key within the state's dates dictionary
			if dateFilter in state_obj.dates:
				payload.append(
					{
						"Country": countryFilter,
						"State": state_key,
						"Date": dateFilter,
						"Types": state_obj.dates[dateFilter].reprJSON(),
					}
				)

	# when country and state is empty
	# in this case, return all the dates, but only use the date given
	elif countryFilter == "" and stateFilter == "" and dateFilter != "":
		for country_key, country_obj in countries_list.items():
			for state_key, state_obj in country_obj.states.items():
				# checking if the date is a key within the state's dates dictionary
				if dateFilter in state_obj.dates:
					payload.append(
						{
							"Country": country_key,  # <- these change
							"State": state_key,  # <- these change
							"Date": dateFilter,  # <- when var is given, this will always be the same so you can just slap it there
							"Types": state_obj.dates[dateFilter].reprJSON(),
						}
					)

	# print(payload)
	# if payload is empty, no results found / api responsed with nothing
	return payload
