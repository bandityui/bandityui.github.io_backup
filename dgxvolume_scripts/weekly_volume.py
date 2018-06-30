import urllib.request
import json
import datetime
from dgxtotalsupply import *

now = datetime.datetime.now()
with open('date.txt','w+') as f:
  f.write(str(now))

# DGX on-chain volume
with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&page=1&offset=999999&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  data = json.loads(url.read().decode())
amount = data.get("result","None")
x = 0
length = len(amount)

# print messages
print("This page updates hourly using data from the [DGX contract address (etherscan)](https://etherscan.io/token/0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf). Last updated:")
print(now.strftime("%Y-%m-%d %H:%M") + ' UTC\n')

# Begin weekly table
print("### Weekly volume table\n")
print("Week Starting | Volume (DGX)")
print("--- | ---")

# loop over whole list of txs
hour = 3600
day  = 24*hour
week = 7*day
quarter = 90*day

# seconds from beginning
d0 = datetime.datetime(2018, 3, 26, 0, 0)
delta = now - d0
ts_now = delta.total_seconds()

wv = 0
qv = 0
datew = d0  # 
dateq = d0  # 
tv = 0
t1 = 0
t2 = 0
cw = 0
cq = 0
tstore1 = 0
tstore2 = 0
t0 = amount[0]['timeStamp']  # time (s) of first tx 
with open('quarterly.dat','w+') as f2:
  with open('weekly.dat','w+') as f:
    for i in range(0,length):
      ts = amount[i]['timeStamp']  # read current timeStamp (s)
      x = int(amount[i]['value'])  # volume for ith tx
      wv = wv + x  # accumulate tx amounts 
      qv = qv + x  # accumulate tx amounts 
      tv = tv + x  # accumulate tx amounts 
      tc = int(ts) - int(t0)  # time (s) since first tx
      t1 = tc - tstore1  # time (s) since last reset
      t2 = tc - tstore2  # time (s) since last reset
      if t1 >= week:
        cw += 1 # count
        y = round(float(wv)/1e9,8)
        print(str(datew.strftime("%d/%m/%Y")) + "|" + str(y))
        f.write(str(datew) + ' ' + str(y) + '\n')  # write week number, volume to file
        datew = datew + datetime.timedelta(days=7)
        tstore1 = tc
        t1 = 0
        wv = 0
      elif t2 >= quarter:
        cq += 1 # count
        y = round(float(qv)/1e9,8)
        f2.write(str(dateq) + ' ' + str(y) + '\n')  # write week number, volume to file
        dateq = dateq + datetime.timedelta(days=90)
        tstore2 = tc
        t2 = 0
        qv = 0

# current (unfinished week) and quarter volume
wv = round(float(wv)/1e9,8)
qv = round(float(qv)/1e9,8)
tv = round(float(tv)/1e9,8)

# All-time volume table
#print("Current Quarter |" + str(dateq.strftime("%d/%m/%Y")) + "|" + str(qv) )
print("\n")
print("### All-time volume\n")
print("Date | Volume (DGX)")
print("--- | ---")
print(str(d0.strftime("%d/%m/%Y"))    + "|" + str(tv) + "\n")

totalsupply = dgxtotalsupply()
print("| DGX Total Supply |")
print("| --- |")
print("|" + totalsupply + "|\n")


