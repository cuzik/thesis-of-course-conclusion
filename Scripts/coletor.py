from datetime import datetime
import json, requests
import ast

def rote_info(origin, destination):
	require_url = ("https://maps.googleapis.com/maps/api/directions/json?"
											+ "origin=place_id:" + origin
											+ "&destination=place_id:" + destination
											+ "&departure_time=now"
											+ "&key=AIzaSyDNFfzulwTdNST376L6sCPaMtvCBYNPbR0")
	content = requests.get(require_url).content
	json_content = json.loads(content)
	json_routs = json_content['routes'][0]
	json_legs = json_routs['legs'][0]
	steps = json_legs['steps']
	return "{'distance':" + str(steps[0]['distance']['value']) + ",'duration':" + str(steps[0]['duration']['value']) + "}\n"


def read_places(file_name):
	places = []
	file_in = open(file_name,'r')
	for line in file_in:
		places += [ast.literal_eval(line)]
	return places

places = read_places('../street_info_from_google')

aux = datetime.now()
atual_minute = (aux.minute - 15 )%60

while True:
	now = datetime.now()
	if now.minute == (atual_minute + 15)%60:
		file_out = open("../Logs/log-" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute),'w')
		file_out.write(rote_info(places[0]['place_id'],places[1]['place_id']))
		for i in range(1,len(places)):
			file_out.write(rote_info(places[i]['place_id'],places[0]['place_id']))
		atual_minute = now.minute