from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
import dateutil.parser as dateparser
import datetime
import requests
import json
from django.utils import timezone



@api_view(['POST', 'GET'])
def post_participation(request):
	if request.method == 'POST':
		try:
			google_id = request.POST.get("google_id", "")
			event_id = request.POST.get("facebook_id", "")
		except:
			return Response({"error": "Couldn't find google_id"})

		person = Person.objects.get(google_id=google_id)

	return Response({"success" : True})


def is_current_event(event):
    try:
        start_time = event["start_time"]
        end_time = event["end_time"]
    except:
        return False

    period = list(map(dateparser.parse, [start_time, end_time]))
    print(period[0], period[1], datetime.datetime.now())
    if period[0] <= timezone.now() <= period[1]:
        return True
    else:
        return False

@api_view(['GET'])
def current_events(request):
    url = "https://va4lqabq07.execute-api.eu-west-1.amazonaws.com/techsoc/events"
    all_events = json.loads(requests.get(url).text)

    current_events = list(filter(lambda k: is_current_event(k), all_events))

    return Response(current_events)

