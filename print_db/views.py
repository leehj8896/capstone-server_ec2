from django.http import HttpResponse
from .models import *
from django.shortcuts import render
import MySQLdb
from django.db import IntegrityError
import base64
import json

def index(request):
    return render(request, 'myserver/index.html')
#return HttpResponse("/event/ /place/ /imply/"dd);

def event(request):

    query = "select * from event"

    return HttpResponse(print_dicts(query));

def imply(request):

    query = "select * from imply"

    return HttpResponse(print_dicts(query))

def place(request):

    query = "select * from place"

    event_id = request.POST.get('event_id', None)
    temp_places_size = request.POST.get('temp_places_size', None)
    
    if event_id != None:
        query += " where event_id = " + event_id
    elif temp_places_size != None:
        query += " where "
        for i in range(int(temp_places_size)):
            temp_place_id = request.POST['temp_places_id' + str(i)]
            query += "place_id = " + temp_place_id
            if i != int(temp_places_size) - 1:
                query += " or "

    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()

    result = ""
    """
    for row in rows:
        result += str(row) + "\n"
    """
    for i in range(len(rows)):
        
        one = "{'place_id': " + str(rows[i]['place_id'])
        one += ", 'place_name': '" + str(rows[i]['place_name'])
        one += "', 'address': '" + str(rows[i]['address'])
        one += "', 'explanation': '" + str(rows[i]['explanation'])
        one += "', 'qr_message': '" + str(rows[i]['qr_message'])
        one += "', 'latitude': " + str(rows[i]['latitude'])
        one += ", 'longitude': " + str(rows[i]['longitude'])
        one += ", 'auth_qr': " + str(rows[i]['auth_qr'])
        one += ", 'becoan_distance': " + str(rows[i]['becoan_distance'])
        one += ", 'auth_gps': " + str(rows[i]['auth_gps'])
        one += ", 'auth_exif': " + str(rows[i]['auth_exif'])
        if rows[i]['picture'] == None:
            one += ", 'picture': 'None'}"
        else:
            basedImage = rows[i]['picture']
            decodedImage = basedImage.decode("UTF-8")
            encodedImage = decodedImage.encode("UTF-8")
            reBasedImage = base64.b64decode(encodedImage)
            reDecodedImage = reBasedImage.decode("UTF-8")
            one += ", 'picture': '" + reDecodedImage + "'}"
        
        result += one
        if i != len(rows) - 1:
            result += "%%%"

    conn.close()
    return HttpResponse(result)

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
def count_query(query):
    
    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rowcount = curs.rowcount
    conn.close()
    return rowcount

def get_query(query,key):
    
    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()
    conn.close()
    return rows[0].get(key)

def insert_event(request):
    
    lastId = Event.objects.all().last().event_id
    event = Event.objects.create(event_id=lastId+1, event_name=request.POST['event_name'], reward=request.POST['reward'], user=User.objects.get(user_id=request.POST['user_id']))
    
    return HttpResponse(lastId + 1)

def insert_place(request):

    lastId = Place.objects.all().last().place_id
    place = Place.objects.create(place_id=lastId+1, place_name=request.POST['place_name'], address=request.POST['address'], explanation=request.POST['explanation'])
    #imply = Imply.objects.create(event_id=Event.objects.all().last().event_id, place_id=Place.objects.all().last().place_id)

    return HttpResponse(lastId + 1)

def insert_imply(request):
    
    eventID = request.POST['event_id']
    placeID = request.POST['place_id']
    imply = Imply.objects.create(event=Event.objects.get(event_id=eventID), place=Place.objects.get(place_id=placeID))
    return HttpResponse(placeID)

def insert_picture(request):

    image_string = request.POST['picture']
    image_bytes = image_string.encode('utf-8')        # 유니코드 >> 바이트
    image_based = base64.b64encode(image_bytes)       # 바이트 >> base64
#image_decoded = image_based.decode("UTF-8")       # base64 >> 유니코드

    lastID = Place.objects.all().last().place_id
    place = Place.objects.get(place_id=lastID)
    place.picture = image_based
    place.save()

    return HttpResponse(image_based)

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

def ranking(request):
    event_id = request.POST['event_id']
    query = 'select * from participation where event_id = "%s" order by number_of_visits desc' % event_id
     
    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'capstone', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()
    result = ""
    for row in rows:
        result += str(row) + "\n"
    conn.close()
    return HttpResponse(result)

def auth(request):
    place_id = int(request.POST['place_id'])
    auth_num = request.POST['auth_num']    
    user_id = request.POST['user_id']
    event_id = int(request.POST['event_id'])
    if auth_num == '1':
        qr_message = request.POST['qr_message']
        query = 'select place_id from place where qr_message = "%s" and place_id = %d' %(qr_message,place_id)
        result = count_query(query)
   
    elif auth_num == '2':
        distance = float(request.POST['becoan_distance'])
        query = 'select becoan_distance from place where place_id = %d' % place_id
        becoan_distance = float(get_query(query,'becoan_distance'))
        if abs(distance-becoan_distance) < 20:
            result = 1
        else:
            result = -1
    elif auth_num == '3':
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        query1 = 'select latitude from place where place_id = %d' % place_id
        query2 = 'select longitude from place where place_id = %d' % place_id
        lt = float(get_query(query1,'latitude'))
        gt = float(get_query(query2, 'longitude'))
        lt = abs(lt-latitude)*1000000
        gt = abs(gt-longitude) * 1000000
        if lt <= 90:
            if gt <= 90:
                result = 1
            else:
                result = -1
        else:
            result = -1  
    else:
        return HttpResponse('error')
    if result == 1:
        query = 'select * from participation where user_id = "%s" and event_id = %d' %(user_id, event_id)
        query2 = 'select * from participation where user_id = "%s" and event_id = %d' %(user_id, event_id)
        query3 = 'select number_of_visits from participation where user_id="%s" and event_id=%d' %(user_id, event_id)
        number_of_visits = get_query(query3,'number_of_visits')+1
        query4 = 'update participation set number_of_visits =%d where user_id = "%s" and event_id=%d' %(number_of_visits,user_id,event_id)
        if count_query(query) < 1:
            return HttpResponse('error')
        else:
            auth = Auth.objects.create(user = User.objects.get(user_id=request.POST['user_id']), event = Event.objects.get(event_id=request.POST['event_id']), auth_place_id = place_id)
            count_query(query4)
            return HttpResponse('ok')
    else:
        return HttpResponse('error')
    
def participate_event(request):
    try:
        participation = Participation.objects.create(user = User.objects.get(user_id=request.POST['user_id']), event = Event.objects.get(event_id=request.POST['event_id']), number_of_visits = 0)           
        return HttpResponse('ok')    
    except IntegrityError:
        return HttpResponse("duplicated")
