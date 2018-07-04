import urllib.request
import json
import datetime

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


# loop over whole list of txs
hour = 3600
day  = 24*hour
week = 7*day
quarter = 90*day

# seconds from beginning
d0 = datetime.datetime(2018, 3, 23, 8, 58)
delta = now - d0
ts_now = delta.total_seconds()
t0 = amount[0]['timeStamp']  # time (s) of first tx 
tlast = amount[length-1]['timeStamp']  # time (s) of first tx 
a = int(ts_now) - (int(tlast) - int(t0))
with open('tsince_lasttx.txt','w+') as f:
  f.write(str(a))

# Begin weekly table
print("### Weekly volume table\n")
print("Week Starting | Volume (DGX)")
print("--- | ---")

with open('weekly.dat','w+') as f:
  wv = 0                                        # weekly volume 
  tv = 0                                        # total volume
  cw = 1                                        # week counter (start at 1)
  t0 = amount[0]['timeStamp']                   # time of first tx
  for i in range(0,length):
    x = int(amount[i]['value'])  # volume for ith tx
    if amount[i]['from'] == '0x0000000000000000000000000000000000000000':  # if from 0x0 (minting)
      mintv = mintv + x  # DGX minted 
    elif amount[i]['to'] == '0x0000000000000000000000000000000000000000':  # if to 0x0 (recasting)
      wv = wv - x  # these are recasting txs
      mintv = mintv - x  
    else:					# else is a normal tx
      ti = amount[i]['timeStamp']               # time of ith tx
      dt = int(ti) - int(t0)                    # seconds since t0
      vi = int(amount[i]['value'])              # volume of ith tx
      wv = wv + vi                              # accumulate weekly volume
      tv = tv + vi                              # accumulate total volume
    if dt >= cw*week:                           # if dt > cw weeks
      cw += 1                                   # +1 week
      di = d0 + datetime.timedelta(seconds=dt)  # datetime of ith tx
      y = round(float(wv)/1e9,2)                # round
      y2 = round(float(mintv)/1e9,2)
      print(str(di.strftime("%d/%m/%Y")) + "|" + str(y))  # print information to file
      f.write(str(di) + ' ' + str(y) + ' ' + str(y2) + '\n')    # write week number, volume to file
      wv = 0                                    # reset weekly volume 
wv = round(float(wv)/1e9,2)                     # current, unfinished week
tv = round(float(tv)/1e9,2)                     # round
y2 = round(float(mintv)/1e9,2)

f.write(str(datew) + ' ' + str(wv) + ' ' + str(y2) + '\n')  # write week number, volume to file
print(str(datew.strftime("%d/%m/%Y")) + "|" + str(wv))

# All-time volume table
#print("Current Quarter |" + str(dateq.strftime("%d/%m/%Y")) + "|" + str(qv) )
print("\n")
print("### All-time volume\n")
print("Starting Date | Volume (DGX)")
print("--- | ---")
tv = round(float(tv)/1e9,2)
print(str(d0.strftime("%d/%m/%Y"))    + "|" + str(tv) + "\n")

print("### Total Supply\n")
print("| DGX Total Supply |")
print("| --- |")
print("|" + y2 + "|\n")


