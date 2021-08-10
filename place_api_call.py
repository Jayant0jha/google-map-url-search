import pandas as pd, numpy as np
import requests
import json
import time

{
    "html_attributions": [],
    "next_page_token": "Aap_uECNDJO2uHLqujAOOZkMmNOym5E6qAw8HY9EjcAqCUBDoNa3kZNsdN5iDF_qy3v85WvFODqAGl4Hl4qhu5XbHp-0QSVsdWltBiMf_Flt4GP7EHx2y49FEVu_NEXxn7iQgNOID93C6QdcyADH4JT9MZb6Bb62NOT861Z9va61Jv5n7J2poVulVKfvBoTvFPLgMQppOb-xFV7tNjCeHt7D5C4JuMoFuBJFB0FwR7PJyIINTKKlsB1xmCjabiAOm0J927PGPbm85VoNvdtJyrtnSgWuxzgM_NSdog3uSRKvLcJ0Dfv-eZUC7HXdJk5rLYkNJ2f4e3p7P-iO189WYNLC9pScCjVWb8Wbqp0KZVB87IUVLNF_bjnAPEEGEcetUSCLbgkPty1NkUgnIPHNNF_Ex0MPrMD8ZmWW4zv2JD9LgeJXZcLaoCGHc0vOwfQA",
    "results": [
        {
            "business_status": "OPERATIONAL",
            "geometry": {
                "location": {
                    "lat": 24.4151928,
                    "lng": 75.8335733
                },
                "viewport": {
                    "northeast": {
                        "lat": 24.4164419802915,
                        "lng": 75.83499448029151
                    },
                    "southwest": {
                        "lat": 24.4137440197085,
                        "lng": 75.83229651970849
                    }
                }
            },
            "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png",
            "icon_background_color": "#FF9E67",
            "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet",
            "name": "Agarwal Namkeen Bhandar",
            "photos": [
                {
                    "height": 480,
                    "html_attributions": [
                        "<a href=\"https://maps.google.com/maps/contrib/112673794500204609782\">Gokul Singh Chouhan Mogra</a>"
                    ],
                    "photo_reference": "Aap_uEBnfLDwJOkBwSZa8Jo7s8odLYc39tNhBUmhknl5rir7pcvXMHbjaORzCH-ny67e9aLJBQ16k7h49wnfhPSa_YB95ljHp-j3RZByIz3PNTZUt8GHjhGIJKd1-rlcRDQD4yf87XMF5S_ASDjBpipFXwtTgXQJ0G63wipEgmJyg75oiSE3",
                    "width": 639
                }
            ],
            "place_id": "ChIJqbYMeYwFZTkRt5gY8kxEAvg",
            "plus_code": {
                "compound_code": "CR8M+3C Bhawani Mandi, Rajasthan, India",
                "global_code": "7JPQCR8M+3C"
            },
            "rating": 2.5,
            "reference": "ChIJqbYMeYwFZTkRt5gY8kxEAvg",
            "scope": "GOOGLE",
            "types": [
                "restaurant",
                "food",
                "point_of_interest",
                "establishment"
            ],
            "user_ratings_total": 4,
            "vicinity": "Ashram Road, Bhawani Mandi"
        },
]}

final_data = []

location='24.4165267,75.833981'
radius='2000'
types='restaurant'
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&key=AIzaSyDRtc7ZR-efB7ISl0vDcShTHQc4COizVDM" % (location,radius,types)

payload={}
headers = {}

while True:
	print(url)
	response = requests.request("POST", url, headers=headers, data=payload)

	response = json.loads(response.text)
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
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&key=AIzaSyDRtc7ZR-efB7ISl0vDcShTHQc4COizVDM%s" % (location,radius,types,next_page_token)

labels = ['Place Name','Place ID', 'Latitude', 'Longitude', 'rating','Types', 'Vicinity']

export_dataframe_1_medium = pd.DataFrame.from_records(final_data, columns=labels)
export_dataframe_1_medium.to_csv('export_dataframe_1_medium.csv')


