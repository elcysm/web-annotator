import json
from urllib.request import urlopen
import datetime as dt
import pytz

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']
timezone=data['timezone']

print('Your IP detail\n' )
print('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \nTimeZone : {5}'.format(org,region,country,city,IP,timezone))

now = dt.datetime.now()

vietnam=pytz.timezone(timezone)

vietnam_now = now.astimezone(vietnam).strftime("%d/%m/%Y %H:%M:%S")
print('Time:',vietnam_now)