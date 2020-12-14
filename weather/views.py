import requests
import datetime
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Weather
from .serializers import WeatherSerializer


query_city = "Berlin"
query_country = "DE"


def get_precipitation(lat, lon):
	key = "39a4f3f89c9d4ebb8c172e431659f57b"
	get_url = "https://api.weatherbit.io/v2.0/current".format()
	params = {"lat": lat, "lon": lon, "key": key}
	r = requests.get(url=get_url, params=params)
	print("-=-=-=-=-=-=-=-=-=-\n", r.json()["data"][0], "\n-=-=-=-=-=-=-=-=-=-")
	return r.json()["data"][0]


def get_current(city, country_code):
	aid = "6a5ad56e3ddc03d99e2d4b4c69d7e457"
	get_url = "http://api.openweathermap.org/data/2.5/weather"
	params = {
		"appid": aid,
		"q": "{},{}".format(city, country_code),
		"units": "metric",
	}
	r = requests.get(url=get_url, params=params)
	return r.json()


class WeatherViewSet(viewsets.ModelViewSet):
	""" API endpoint that allows for GET requests on weather """
	authentication_classes = []
	permission_classes = []
	serializer_class = WeatherSerializer
	queryset = Weather.objects.all()

	@action(detail=False, methods=['get'])
	def current(self, request, *args, **kwargs):
		global query_city, query_country
		if "city" in request.query_params:
			query_city = request.query_params["city"]
		if "country" in request.query_params:
			query_country = request.query_params["country"]
		queryset = Weather.objects.filter(city_name__iexact=query_city)
		if (
			queryset.exists() and (
				(
					datetime.datetime.now() -
					queryset.order_by('-date_taken')[0]
					.date_taken.replace(tzinfo=None)
				).seconds // 60 <= 15
			)
		):
			obj = queryset.order_by('-date_taken')[0]
		else:
			json = get_current(query_city, query_country)
			prec = get_precipitation(
				json["coord"]["lon"],
				json["coord"]["lat"],
			)
			obj = Weather(
				city_id=json["id"],
				city_name=json["name"],
				temperature=json["main"]["temp"],
				humidity=json["main"]["humidity"],
				t_min=json["main"]["temp_min"],
				t_max=json["main"]["temp_max"],
				utc_time=json["dt"],
				precipitation=prec["precip"] if prec["precip"] else 0,
				solar_rad=prec["solar_rad"] if prec["solar_rad"] else 0,
			)
			obj.save()

		serializer = WeatherSerializer(obj, many=False)
		return Response(serializer.data)


def weather_city(request):
	global query_city, query_country
	params = request.GET
	if "city" in params:
		query_city = params["city"]
	if "country" in params:
		query_country = params["country"]
	queryset = Weather.objects.filter(city_name__iexact=query_city)
	if queryset.exists():
		obj = queryset.order_by('-date_taken')[0]
	else:
		return HttpResponseNotFound('<h1>Cidade sem dados</h1>')

	return HttpResponse(
		'''<html>
			<h1>Tempo em {}</h1>
			<br>
			Temperatura: {}ºC<br>
			Temp. máxima: {}ºC<br>
			Temp. mínima: {}ºC<br>
			Umidade: {}%<br>
			Radiação solar: {}W/m<sup>2</sup><br>
			Precipitação: {}mm/hr<br>
			Dados obtidos em {}<br>
			<br>
			Escolha cidade para nova consulta
			<form action="/weather_at_city" method="get">
				<label for="city">Cidade:</label>
				<input type="text" id="city" name="city"><br><br>
				<label for="country">País:</label>
				<input type="text" id="country" name="country"><br><br>
				<input type="submit" value="Enviar">
			</form>
		</html>'''
		.format(
			query_city,
			obj.temperature,
			obj.t_min,
			obj.t_max,
			obj.humidity,
			obj.solar_rad,
			obj.precipitation,
			obj.date_taken.strftime("%d/%m/%Y, %H:%M:%S"),
		)
	)
