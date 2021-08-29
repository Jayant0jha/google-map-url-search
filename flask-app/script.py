from flask import Flask, redirect, url_for, render_template, request
import pandas as pd, numpy as np
import requests
import json
import time


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



def place_api_call(location,types,radius='2000'):

	final_data = []
	
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&key=AIzaSyBF5ZAK0oC3eyuxl0ATY-t_hVQfts1P4WI" % (location,radius,types)

	payload={}
	headers = {}

	while True:
		print(url)
		response = requests.request("POST", url, headers=headers, data=payload)

		response = json.loads(response.text)
		print(response)
		results = response['results']
		for result in results:
			print(result)
			name = result['name']
			place_id = result ['place_id']
			lat = result['geometry']['location']['lat']
			lng = result['geometry']['location']['lng']
			rating = result.get('rating',0)
			types = result['types']
			vicinity = result['vicinity']
			data = [name, place_id, lat, lng, rating, types, vicinity]
			final_data.append(data)
		#time.sleep(5)
		if 'next_page_token' not in response:
			break
		else:
			next_page_token = response['next_page_token']
		next_page_token = '&pagetoken=%s' % str(next_page_token)
		url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&key=AIzaSyBF5ZAK0oC3eyuxl0ATY-t_hVQfts1P4WI%s" % (location,radius,types,next_page_token)

	labels = ['Place Name','Place ID', 'Latitude', 'Longitude', 'rating','Types', 'Vicinity']

	export_dataframe_1_medium = pd.DataFrame.from_records(final_data, columns=labels)
	export_dataframe_1_medium.to_csv('export_dataframe_1_medium.csv')
app = Flask(__name__)



@app.route("/", methods=["POST", "GET"])
def runScript():
	if request.method == "POST":
		url = request.form["url"]
		print("url: ",url)
		url_parts =  url.split('/@')
		lat_long = url_parts[1].split(',')
		location = "%s,%s" % (str(lat_long[0]),str(lat_long[1]))
		types = []
		for type in all_types:
			if type in url and type not in types:
				types.append(type)
		query_type = ",".join(types)
		place_api_call(location,query_type)
		return redirect(url_for("download", data=url))
	else:
		return render_template("form.html")

@app.route("/download/<path:data>/")
def download(data):
    return f"<h1>{data}</h1>"

if __name__ == "__main__":
    app.run()
