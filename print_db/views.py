from django.http import HttpResponse
from .models import Event
from .models import Place
import MySQLdb

def index(request):
    return HttpResponse("/event/ /place/ /imply/");

def event(request):

    query = "select * from event"

    return HttpResponse(print_dicts(query));

def imply(request):

    query = "select * from imply"

    return HttpResponse(print_dicts(query))

def place(request):

    query = "select * from place"

    return HttpResponse(print_dicts(query))

def print_dicts(query):

    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()

    result = ""
    for row in rows:
        result += str(row) + "\n"
    conn.close()

    return result

def insert_event(request):
    
    lastId = Event.objects.all().last().event_id
    event = Event.objects.create(event_id = lastId + 1, event_name = request.POST['event_name'])
    
    return HttpResponse()

def insert_place(request):

    lastId = Place.objects.all().last().place_id
    event = Place.objects.create(place_id = lastId + 1, place_name = 'place name')

    return HttpResponse()
