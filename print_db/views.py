from django.http import HttpResponse
import MySQLdb

def index(request):
    return HttpResponse("/event/ /place/ /event_has_place/");

def event(request):

    query = "select * from event"

    return HttpResponse(print_dicts(query));

def event_has_place(request):

    query = "select * from event_has_place"

    return HttpResponse(print_dicts(query))

def place(request):

    query = "select * from place"

    return HttpResponse(print_dicts(query))

def print_dicts(query):

    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'mydb', charset='utf8')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()

    result = ""
    for row in rows:
        result += str(row) + "\n"
    conn.close()

    return result
