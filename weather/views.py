import requests
from .models import Weather
from .serializers import WeatherSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


def get_current(city, country_code):
	get_url = "http://api.openweathermap.org/data/2.5/weather"
	headers = {}
	params = {
		"appid": "6a5ad56e3ddc03d99e2d4b4c69d7e457",
		"q": "{},{}".format(city, country_code),
		"units": "metric",
	}
	r = requests.get(url=get_url, headers=headers, params=params)
	return r.json()


class WeatherViewSet(viewsets.ModelViewSet):
	""" API endpoint that allows for GET requests on weather """
	authentication_classes = []
	permission_classes = []
	serializer_class = WeatherSerializer
	queryset = Weather.objects.all()

	@action(detail=False, methods=['get'])
	def current(self, request, *args, **kwargs):
		print("FLAG Q1", request.query_params)
		query_city = "Berlin"
		query_country = "DE"
		if "city" in request.query_params:
			query_city = request.query_params["city"]
		if "country" in request.query_params:
			query_country = request.query_params["country"]
		json = get_current(query_city, query_country)
		obj = Weather(
			city_id=json["id"],
			city_name=json["name"],
			temperature=json["main"]["temp"],
			humidity=json["main"]["humidity"],
		)
		obj.save()
		queryset = obj
		serializer = WeatherSerializer(queryset, many=False)
		return Response(serializer.data)
