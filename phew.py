import urllib
import urllib2
from StringIO import StringIO
import gzip
import json
from random import randrange
from time import sleep
from settings import *
from datetime import datetime, timedelta

# Set to true to print debug logs
DEBUG = False

# Refresh scan
refresh_url = 'http://v4api.phewtick.com/meets/refresh'

# Scan on meet
scan_url = 'http://v4api.phewtick.com/meets/meet'

# Post location
post_location_url = 'http://v4api.phewtick.com/users/position'


headers = { 'User-Agent' : 'Phewtick/3.1.0 (iPhone; iOS 6.0.1; Scale/2.00)',
            'Accept' : 'application/json',
            'Accept-Language' : 'en, zh-Hant, ar, zh-Hans, fr, de, ja, nl, it, es, pt-PT, da, fi, nb, sv, ko, ru, pl, pt, tr, uk, hr, cs, el, he, ro, sk, th, id, ms, en-GB, ca, hu, vi, en-us;q=0.8',
            'Proxy-Connection' : 'keep-alive',
            'Accept-Encoding' : 'gzip, deflate'}

headers_form = headers
headers_form['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'


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


def updateLocation(token):
    values = {'lng' : lng,
          'lat' : lat,
          'tz_offset' : tz_offset,
          'tz_id' : tz_id, 
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





# Start the hack engine (:
while (True):
    # Loop from 1st till second last token
    for i in range(0, len(tokens)-1):
        # Loop for from next till last
        for j in range(i+1, len(tokens)):
            new_qr_key = refreshToken(tokens[j])
            sleep(randrange(10))
            scanToken(tokens[i], new_qr_key)
            sleep(randrange(10))
        sleep(randrange(20))

    # Sleep for 1 hour
    t = 60*60
    print "Sleeping for " + str(t/60) + " minutes.."
    next = datetime.now() + timedelta(0,t)
    print "Next meetup at " + next.strftime('%H:%M')
    sleep(t)

    # Update everybody location
    for i in range(0, len(tokens)):
        updateLocation(tokens[i])
        sleep(randrange(10))
    


