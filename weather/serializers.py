from .models import Weather
from rest_framework import serializers


class WeatherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Weather
		fields = [
			'city_id',
			'city_name',
			'date_taken',
			'temperature',
			'humidity',
		]
