import urllib.request
import json
import datetime

# DGX on-chain volume
with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&page=1&offset=999999&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  data = json.loads(url.read().decode())
amount = data.get("result","None")
length = len(amount)

# print messages
print("This page updates hourly using data from the [DGX contract address (etherscan)](https://etherscan.io/token/0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf). Last updated:")
now = datetime.datetime.now()			# current time
print(now.strftime("%Y-%m-%d %H:%M") + ' UTC\n')


# loop over whole list of txs
hour = 3600
day  = 24*hour
week = 7*day
quarter = 90*day


# Begin weekly table
print("### Daily volume table\n")
print("Week Starting | Volume (DGX)")
print("--- | ---")

t0 = int(amount[0]['timeStamp'])	        # time (s) of first tx 
tlast = amount[length-1]['timeStamp']           # time (s) of last tx 
dt = int(tlast) - int(t0)			# time between 1st and last txs
d0 = now - datetime.timedelta(seconds=dt)	# approx. time of 1st tx 
di = d0
with open('daily.dat','w+') as f:		# open file for writing
  dv = 0                                        # weekly volume 
  tv = 0                                        # total volume
  cd = 1                                        # week counter (start at 1)
  ts = 0					# total supply
  for i in range(0,length):
    vi = int(amount[i]['value'])                # volume of ith tx
    ti = int(amount[i]['timeStamp'])	        # time of ith tx
    dt = ti - t0	                        # seconds since t0
    if amount[i]['from'] == '0x0000000000000000000000000000000000000000':  # if from 0x0 (minting)
      ts = ts + vi  # DGX minted 
    elif amount[i]['to'] == '0x0000000000000000000000000000000000000000':  # if to 0x0 (recasting)
      dv = dv - vi  # these are recasting txs
      tv = tv - vi
      ts = ts - vi  
    else:					# else is a normal tx
      dv = dv + vi                              # accumulate weekly volume
      tv = tv + vi                              # accumulate total volume
    if dt > cd*day:                             # if dt > cd days
      print('dt = ' + str(float(dt/day)) + ', cd = ' + str(cd))
      cd = int(dt/day + cd) + 1                     # +n days
      y = round(float(dv)/1e9,2)                # round
      y2 = round(float(ts)/1e9,2)
      print(str(di.strftime("%d/%m/%Y")) + "|" + str(y))  # print information to file
      f.write(str(di) + ' ' + str(y) + ' ' + str(y2) + '\n')    # write week number, volume to file
      di = d0 + datetime.timedelta(seconds=dt)  # datetime of ith tx
      dv = 0                                    # reset weekly volume 
  dv = round(float(dv)/1e9,2)                     # current, unfinished week
  tv = round(float(tv)/1e9,2)                     # round
  y2 = round(float(ts)/1e9,2)
  f.write(str(di) + ' ' + str(dv) + ' ' + str(y2) + '\n')  # write week number, volume to file
print(str(di.strftime("%d/%m/%Y")) + "|" + str(dv))

# All-time volume table
#print("Current Quarter |" + str(dateq.strftime("%d/%m/%Y")) + "|" + str(qv) )
print("\n")
print("### All-time volume\n")
print("Starting Date | Volume (DGX)")
print("--- | ---")
print(str(d0.strftime("%d/%m/%Y"))    + "|" + str(tv) + "\n")

print("### Total Supply\n")
print("| DGX Total Supply |")
print("| --- |")
print("|" + str(y2) + "|\n")


