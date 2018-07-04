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
tblock = 14.4
hour = 3600/tblock
day  = 24*hour
week = 7*day
quarter = 90*day

# seconds from beginning
d0 = datetime.datetime(2018, 3, 26, 0, 0)
delta = now - d0
ts_now = delta.total_seconds()

wv = 0
tv = 0
datew = d0
mintv = 0
b1 = 0
cw = 0
bstore1 = 0
b0 = amount[0]['blockNumber']  # block number of first tx 
with open('quarterly.dat','w+') as f2:
  with open('weekly.dat','w+') as f:
    for i in range(0,length):
      x = int(amount[i]['value'])  # volume for ith tx
      if amount[i]['from'] == '0x0000000000000000000000000000000000000000':  # if from 0x0 (minting)
        mintv = mintv + x  # DGX minted 
      elif amount[i]['to'] == '0x0000000000000000000000000000000000000000':  # if to 0x0 (recasting)
        wv = wv - x  # these are recasting txs
        mintv = mintv - x  
        bs = amount[i]['blockNumber']  # read current block number
        bc = int(bs) - int(b0)  # blocks since first tx
        b1 = bc - bstore1  # blocks since last reset
      else:
        bs = amount[i]['blockNumber']  # read current block number
        wv = wv + x  # accumulate tx amounts 
        tv = tv + x  # accumulate tx amounts 
        bc = int(bs) - int(b0)  # blocks since first tx
        b1 = bc - bstore1  # blocks since last reset
      if b1 >= week:
        cw += 1 # count
        y = round(float(wv)/1e9,2)
        print(str(datew.strftime("%d/%m/%Y")) + "|" + str(y))
        y2 = round(float(mintv)/1e9,2)
        f.write(str(datew) + ' ' + str(y) + ' ' + str(y2) + '\n')  # write week number, volume to file
        datew = datew + datetime.timedelta(days=7)
        bstore1 = bc
        b1 = 0
        wv = 0
    wv = round(float(wv)/1e9,2)
    y2 = round(float(mintv)/1e9,2)
    f.write(str(datew) + ' ' + str(wv) + ' ' + str(y2) + '\n')  # write week number, volume to file
    print(str(datew.strftime("%d/%m/%Y")) + "|" + str(wv))
    tv = round(float(tv)/1e9,2)

# All-time volume table
#print("Current Quarter |" + str(dateq.strftime("%d/%m/%Y")) + "|" + str(qv) )
print("\n")
print("### All-time volume\n")
print("Starting Date | Volume (DGX)")
print("--- | ---")
print(str(d0.strftime("%d/%m/%Y"))    + "|" + str(tv) + "\n")

print("### Total Supply\n")
totalsupply = dgxtotalsupply()
print("| DGX Total Supply |")
print("| --- |")
print("|" + totalsupply + "|\n")

