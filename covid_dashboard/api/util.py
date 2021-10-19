from .data_layer.load_csv import *


def Reverse_String(dict):

	payload = dict["payload_bus"]

	payload = str(payload[::-1])

	payload = payload.replace("'", '"')

	return payload


# SNo,ObservationDate,Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered
#Create(Country: USA, State: California, Confirmed : 0, Deaths: 0, Recovered: 0, Date: 9/11/2021)


def Create_Csv(country, state, confirmed, deaths, recovered, date):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()
	#if country is not in the tmp list
	#then we can just append to the dictionary becasuse that country doesn't exist
	#else it exists
	#then use that country as a key and append to that 

	#this checks if the country is in the country list dictionary
	if country in tmp_countries_list:
		#date_obj is a date object that will be added to the country list
		date_obj = Date( date,confirmed, deaths, recovered) 
		#since the country doesn't exist all we need to do is add the 
		#information based on the parameters
		tmp_countries_list[country].states[state].date[state] = date_obj

	else:
		#the country doesn't exist  so need to make a country object
		country_obj = Country(country)
		#then make a date object to add to the country object
		date_obj = Date( date,confirmed, deaths, recovered)
		#sets country object dates to the date object
		country_obj.states[state].date[state] = date_obj
		#finally add the country object to the countries list 
		#based on the country parameter from user 
		tmp_countries_list[country] = country_obj
	
	#back in the load_csv.py 
	#will set the countries_data to tmp_countries_list so we can use the updated data 
	data_layer.set_countries(tmp_countries_list)

def Delete_Csv(country, state, type, date):
	from .urls import data_layer
	tmp_countries_list = data_layer.get_countries()

	#this checks if the country is in the country list dictionary
	#for key in tmp_countries_list:
	if country in tmp_countries_list:
		if state in tmp_countries_list[country].states:
			if date in tmp_countries_list[country].states[state].dates:
				print(tmp_countries_list[country].states[state].dates[date])
				del tmp_countries_list[country].states[state].dates[date]
				print(tmp_countries_list[country].states[state].dates[date])
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
