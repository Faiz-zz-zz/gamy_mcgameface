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

        try:
            event = Event.objects.get(facebook_id=event_id)
            person = Person.objects.get(google_id=google_id)
        except:
            return Response({"error" : "Something went horribly wrong"})

        person.events_attended.add(event)
        person.points += event.points
        person.save()
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
    all_events.append({
        "name": "Hack the North 2016",
        "end_time": "2016-09-19T20:00:00+0100",
        "start_time": "2016-09-16T10:00:00+0100",
        "description": """The University of Waterloo Engineering is home to Canada’s largest engineering school — a pipeline for engineering talent for the world’s leading companies. Ranked among the top 50 engineering schools in the world, the school’s reputation for excellence is built on the foundation of co-op education and a bold history of innovation.""",
        "id": "1751637811790081",
        "place": {
        "name": "UCL",
        "location": {
               "country": "Canada",
               "street": "Waterloo",
               "latitude": 51.524342470225,
               "longitude": -0.13407040013093,
               "zip": "CT14 9",
               "city": "Ontario"
        },
        "id": "92637159209"
     }
    })
    #updating the events model at every query
    for event in all_events:
        try:
            Event.objects.get(facebook_id=event["id"])
        except:
            desc = event["description"] if "description" in event else "No description"

            instance = Event(facebook_id=event["id"], event_name=event["name"], event_description=desc)
            instance.save()


    current_events = list(filter(lambda k: is_current_event(k), all_events))

    return Response(current_events)


@api_view(['POST'])
def register_user(request):
    try:
        google_id = request.POST["google_id"]
        name = request.POST["name"]
    except:
        return Response({"error" : "Parsing data failed"})

    try:
        person = Person.objects.get(google_id=google_id)
    except:

        instance = Person(google_id=google_id, name=name)

        instance.save()

        return Response({"success" : True})

    return Response({"success" : False})


