from django.http import HttpResponse
from .models import *
from django.shortcuts import render
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
    event = Event.objects.create(event_id=lastId+1, event_name=request.POST['event_name'], reward=request.POST['reward'], user=User.objects.get(user_id=request.POST['user_id']))
    
    return HttpResponse()


def insert_place(request):

    lastId = Place.objects.all().last().place_id
    place = Place.objects.create(place_id=lastId+1, place_name=request.POST['place_name'], address=request.POST['address'], explanation=request.POST['explanation'])
    imply = Imply.objects.create(event_id=Event.objects.all().last().event_id, place_id=Place.objects.all().last().place_id)

    return HttpResponse()

def insert_user(request):
    try:
        
        user = User.objects.create(user_id=request.POST.get('user_id'),user_password='',user_email='',user_information=request.POST['user_information'])
        return HttpResponse('success')
    except IndentationError:
        return HttpResponse("There is duplicate id")
    except Exception as e:
       return HttpResponse(e)

def insert_user_direct(request):
    try:
        user = User.objects.create(user_id=request.POST.get('user_id'),user_password=request.POST.get("user_password"),user_email='',user_information=request.POST['user_information'])
        return HttpResponse('success')
    except IndentationError:
        return HttpResponse("There is duplicate id");
    except Exception as e:
        return HttpResponse(e)

def id_duplicate_check(request):
            id = request.POST['user_id']
            query = 'select user_id, count(*) from user where user_id = "%s" group by user_id' % id
            conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute(query)
            rowcount = curs.rowcount
            if(rowcount ==0):
                return HttpResponse('ok')
            else:
                return HttpResponse('error')

def login(request):
    id = request.POST['user_id']
    password = request.POST['user_password']
    query = 'select user_id, user_password from user where user_id="%s" and user_password="%s";' %(id,password)
    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rowcount = curs.rowcount
    if(rowcount == 0):
        return HttpResponse('error')
    else:
        return HttpResponse('ok')

def participate_event(request):

    participation = Participation.objects.create(user=User.objects.get(user_id=request.POST['user_id']), event=Event.objects.get(event_id=request.POST['event_id']))
