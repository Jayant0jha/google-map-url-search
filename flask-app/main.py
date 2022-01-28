import re
from flask import Flask, redirect, url_for, render_template, request, Response
import pandas as pd, numpy as np
import requests
import json
import time
import environment

# https://www.google.com/maps/search/restaurants+near+me/@28.3820803,79.4218832,16z/data=!3m1!4b1
all_types = ['accounting','airport','amusement_park','aquarium','art_gallery','atm','bakery','bank','bar','beauty_salon','bicycle_store',
            'book_store','bowling_alley','bus_station','cafe','campground','car_dealer','car_rental','car_repair','car_wash','casino','cemetery',
			'church','city_hall','clothing_store','convenience_store','courthouse','dentist','department_store','doctor','drugstore','electrician',
			'electronics_store','embassy','fire_station','florist','funeral_home','furniture_store','gas_station','gym','hair_care','hardware_store',
			'hindu_temple','home_goods_store','hospital','insurance_agency','jewelry_store','laundry','lawyer','library','light_rail_station','liquor_store',
			'local_government_office','locksmith','lodging','meal_delivery','meal_takeaway','mosque','movie_rental','movie_theater','moving_company','museum',
			'night_club','painter','park','parking','pet_store','pharmacy','physiotherapist','plumber','police','post_office','primary_school','real_estate_agency',
			'restaurant','roofing_contractor','rv_park','school','secondary_school','shoe_store','shopping_mall','spa','stadium','storage','store','subway_station',
			'supermarket','synagogue','taxi_stand','tourist_attraction','train_station','transit_station','travel_agency','university','veterinary_care','zoo']

api_key = environment.api_key

def place_api_call(query,radius='2000'):
	# _types = types

	final_data = []
	
	# url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&key=AIzaSyAQa-eBVTNTVRal6MszUesc9mQHVD9BasA" % (location,radius,_types)
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s" % (query, api_key)
	payload={}
	headers = {}

	while True:
		print(url)
		response = requests.request("POST", url, headers=headers, data=payload)

		response = json.loads(response.text)
		print('status', response['status'])
		if response['status'] == 'OK':
			print('length',len(response['results']))
			results = response['results']
			for result in results:
				# print(result)
				name = result['name'] if 'name' in result else ''
				address = result['formatted_address'] if 'formatted_address' in result else ''
				phone_number = result['formatted_phone_number'] if 'formatted_phone_number' in result else ''
				intl_number = result['international_phone_number'] if 'international_phone_number' in result else ''
				business_status = result['business_status'] if 'business_status' in result else ''
				# place_id = result ['place_id']
				lat = result['geometry']['location']['lat']
				lng = result['geometry']['location']['lng']
				rating = result.get('rating',0)
				types = result['types'] if 'types' in result else ''
				vicinity = result['vicinity'] if 'vicinity' in result else ''
				place_url = result['url'] if 'url' in result else ''
				website = result['website'] if 'website' in result else ''

				place_detail_url = 'https://maps.googleapis.com/maps/api/place/details/json?fields=formatted_phone_number,international_phone_number,website,url&place_id=%s&key=%s' % (result['place_id'], api_key)
				print('place detail url\n', url)
				place_detail_res = requests.request("POST", place_detail_url, headers=headers, data=payload)

				place_detail_res = json.loads(place_detail_res.text)
				print('status', place_detail_res['status'])
				if place_detail_res['status'] == 'OK':
					place_detail_results = place_detail_res['result']
					print('place detail result\n', place_detail_results)
					phone_number = place_detail_results['formatted_phone_number'] if 'formatted_phone_number' in place_detail_results else ''
					intl_number = place_detail_results['international_phone_number'] if 'international_phone_number' in place_detail_results else ''
					print('ph no.\n', phone_number)
					place_url = place_detail_results['url'] if 'url' in place_detail_results else ''
					website = place_detail_results['website'] if 'website' in place_detail_results else ''

				data = [name, phone_number, intl_number, address, business_status, lat, lng, rating, place_url, website, types, vicinity]
				final_data.append(data)
			#time.sleep(5)
			print('next page token present\n' if 'next_page_token' in response else 'not present next page token\n')
			if 'next_page_token' not in response:
				break
			else:
				next_page_token = response['next_page_token']
				time.sleep(2)
			next_page_token = '&pagetoken=%s' % str(next_page_token)
			print(query,radius,types,next_page_token)
			url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s%s" % (query, api_key, next_page_token)
		else: 
			return None, response['error_message']
	labels = ['Place Name', 'Local Phone No.', 'Internation Phone No.', 'Address', 'Status', 'Latitude', 'Longitude', 'rating', 'URL', 'Website', 'Types', 'Vicinity']

	export_dataframe_1_medium = pd.DataFrame.from_records(final_data, columns=labels)
	return export_dataframe_1_medium.to_csv(), None
	# with open("near_by_me.csv") as fp:
	# 	csv = fp.read()
	# return csv
	


app = Flask(__name__)



@app.route("/", methods=["POST", "GET"])
def runScript():
	if request.method == "POST":
		query = request.form["searchText"]
		print("query: ",query)
		# url_parts =  url.split('/@')
		# lat_long = url_parts[1].split(',')
		# location = "%s,%s" % (str(lat_long[0]),str(lat_long[1]))
		# types = []
		# for type in all_types:
		# 	if type in url and type not in types:
		# 		types.append(type)
		# query_type = ",".join(types)
		csv, error = place_api_call(query)
		# return redirect(url_for("download", data=url))
		if csv:
			return Response(
			csv,
			mimetype="text/csv",
			headers={"Content-disposition":
					"attachment; filename=nearby_places.csv"})
		elif error:
			return render_template("form.html", error=error)
	else:
		return render_template("form.html")

@app.route("/download/<path:data>/")
def download(data):
    return f"<h1>{data}</h1>"

if __name__ == "__main__":
    app.run()
