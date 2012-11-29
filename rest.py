import urllib
import urllib2
from StringIO import StringIO
import gzip
import json
from settings import *
from datetime import datetime, timedelta
from pprint import pprint


# Set to true to print debug logs
DEBUG = False

# API Endpoints
# Refresh scan
refresh_url = 'http://v4api.phewtick.com/meets/refresh'
# Scan on meet
scan_url = 'http://v4api.phewtick.com/meets/meet'
# Post location
post_location_url = 'http://v4api.phewtick.com/users/position'

# New 
# GET http://v4api.phewtick.com/alert/check?token=MY_TOKEN&version=3%2E2%2E0&type=i

# POST http://v4api.phewtick.com/users/active

# GET http://v4api.phewtick.com/users/read?user_id=MY_USER_ID&token=MY_TOKEN

# POST http://v4api.phewtick.com/users/update
# fb_token:        FACEBOOK_TOKEN
# user_id:         MY_USER_ID                                                                                                                                                                      
# expire:          4001-01-01 00:00:00 +0000                                                                                                                                                   
# iphone_version:  3.2.0                                                                                                                                                                       
# token:           MY_TOKEN 


# GET timeline
timeline_url = 'http://v4api.phewtick.com/reports/timeline'

# POST http://v4api.phewtick.com/messages/opened
# toId:   448325                                                                                                                                                                               
# token:  MY_TOKEN


# POST a new message
message_create_url = 'http://v4api.phewtick.com/messages/create'
   

# GET http://v4api.phewtick.com/messages/thread?offset=0&token=MY_TOKEN&limit=21&toId=448325




headers = { 'User-Agent' : 'Phewtick/3.2.0 (iPhone; iOS 6.0.1; Scale/2.00)',
            'Accept' : 'application/json',
            'Accept-Language' : 'en, zh-Hant, ar, zh-Hans, fr, de, ja, nl, it, es, pt-PT, da, fi, nb, sv, ko, ru, pl, pt, tr, uk, hr, cs, el, he, ro, sk, th, id, ms, en-GB, ca, hu, vi, en-us;q=0.8',
            'Proxy-Connection' : 'keep-alive',
            'Accept-Encoding' : 'gzip, deflate'}

headers_form = headers
headers_form['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'

# Some parameters
post_bg = 0







# Returns a new QR code
def refreshToken(token):
    values = {'lng' : lng,
          'lat' : lat,
          'tz_offset' : tz_offset,
          'tz_id' : tz_id,
          'token' : token }
    # refresh_url = 'http://v4api.phewtick.com/meets/refresh?tz_offset=480&lng=103%2E876020&lat=1%2E329576&tz_id=Asia%2FSingapore&token='

    req = urllib2.Request(refresh_url + '?' + urllib.urlencode(values), headers = headers)
    response = urllib2.urlopen(req)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    
    if DEBUG:
        print data
    qr = json.loads(data)['qr_key']
    # print 'Refresh QR: ' + qr

    return qr


# Scan a friend QR Code to register meetup
def scanToken(token, qr_key):
    values = {'lng' : lng,
          'lat' : lat,
          'qr_key' : qr_key, 
          'token' : token }
     
    data = urllib.urlencode(values)
    req = urllib2.Request(scan_url, data, headers)
    response = urllib2.urlopen(req)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    
    if DEBUG:
        print data
    res = json.loads(data)
    
    if 'get_point' in res:
        print '>> Earned ' + str(res['get_point'])
    else:
        if 'err_text' in res:
            print 'Error: ' + str(res['err_text'])
        else:
            print '.'


# Update current location
def updateLocation(token):
    values = {'lng' : lng,
          'lat' : lat,
          'tz_offset' : tz_offset,
          'tz_id' : tz_id, 
          'post_bg' : post_bg,
          'token' : token }
     
    data = urllib.urlencode(values)
    req = urllib2.Request(post_location_url, data, headers_form)
    response = urllib2.urlopen(req)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    
    print '^ ' + data


# Send a message to a Phewtick user
def sendMessage(token, to_id, message):
    values = {'toId' : to_id,
          'body' : message,
          'token' : token }
     
    data = urllib.urlencode(values)
    req = urllib2.Request(message_create_url, data, headers_form)
    response = urllib2.urlopen(req)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    
    print '>> ' + data


# Get timeline of meetups
def getTimeline(token, offset):
    # timeline id is an item. leave empty to start from latest
    # http://v4api.phewtick.com/reports/timeline?token=MY_TOKEN&id=18106425&limit=21&offset=140

    values = {'limit' : 1000,
          'offset' : offset,
          'token' : token }
     
    data = urllib.urlencode(values)
    req = urllib2.Request(timeline_url + '?' + data, None, headers_form)
    response = urllib2.urlopen(req)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    
    timeline = json.loads(data)
    # pprint(j)


    # print '>> ' + data
    return timeline





#######################################
#########       Helpers       #########
#######################################


def writeAllUsersInTimeline(token):
    """
    Read the whole timeline, and write the details of users to file
    """
    timeline = getTimeline(token, 0)

    # Loop thru timeline and print distinct id
    users = {}
    for item in timeline:
        if item['friend']['id'] not in users:
            users[item['friend']['id']] = item['friend']
            # print item['friend']['id'] + ",     # " + item['friend']['name'] 
        if item['other']['id'] not in users:
            users[item['other']['id']] = item['other']
            # print item['other']['id'] + ",     # " + item['other']['name'] 
        
    file = open("./data/users-" + token + ".json", "w+")
    json.dump(users, file)
    file.close()

    return users


def writeAllUsersInTimelineForAllTokens():
    for token in tokens:
        writeAllUsersInTimeline(token)
    return


def readAllUsers(token):
    file = open("./data/users-" + token + ".json", "r")
    data = json.load(file)
    file.close()

    pprint(data)
    return data


def readAllUsersForAllTokens():
    merged = {}
    for token in tokens:
        try:
            users = readAllUsers(token)
            merged = dict(merged.items() + users.items())
        except Exception, e:
            raise e
    return merged






