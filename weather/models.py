from django.db import models


class Weather(models.Model):
	city_id = models.IntegerField(default=0)
	city_name = models.CharField(max_length=50, default="")
	temperature = models.FloatField(default=0)
	t_max = models.FloatField(default=0)
	t_min = models.FloatField(default=0)
	humidity = models.FloatField(default=0)
	date_taken = models.DateTimeField(auto_now_add=True, null=True)
	utc_time = models.IntegerField(default=0)
	precipitation = models.FloatField(default=0)
	solar_rad = models.FloatField(default=0)

	def __str__(self):
		return "id:{}, at:{}, temp:{}, time:{}".format(self.id, self.city_name, self.temperature, self.date_taken)
