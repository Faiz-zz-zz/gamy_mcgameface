from django.db import models

# Create your models here.
class Person(models.Model):
	google_id = models.CharField(unique=True, max_char=100)
	name = models.CharField(max_char=1000)
	event_relation = models.CharField(max_char=1000)
	points = models.IntegerField(default=0)
	events_attended = models.ManyToManyField(related_name='events', blank=True)


class Event(models.Model):
	event_name = models.CharField(max_length=1000)
	event_description = models.CharField(max_length=1000)
	facebook_id = models.CharField(max_length=100, unique=True)
