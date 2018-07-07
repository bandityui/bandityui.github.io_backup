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
length = len(amount)

# print messages
print("This page updates hourly using data from the [DGX contract address (etherscan)](https://etherscan.io/token/0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf). Last updated:")
print(now.strftime("%Y-%m-%d %H:%M") + ' UTC\n')

# loop over whole list of txs
hour = 3600
day  = 24*hour
week = 7*day
quarter = 90*day

# Begin weekly table
print("### Weekly volume table\n")
print("Week Starting | Volume (DGX)")
print("--- | ---")

t0 = int(amount[0]['timeStamp'])	        # time (s) of first tx 
tlast = amount[length-1]['timeStamp']           # time (s) of last tx 
dt = int(tlast) - int(t0)			# time between 1st and last txs
d0 = now - datetime.timedelta(seconds=dt)	# current time minus dt
di = d0
with open('weekly.dat','w+') as f:		# open file for writing
  wv = 0                                        # weekly volume 
  vdigix = 0					# volume from digix marketplace
  tv = 0                                        # total volume
  cw = 1                                        # week counter (start at 1)
  ts = 0					# total supply
  tx = 0					# tx fees
  for i in range(0,length):
    vi = int(amount[i]['value'])                # volume of ith tx
    ti = int(amount[i]['timeStamp'])	        # time of ith tx
    dt = ti - t0	                        # seconds since t0
    ato = amount[i]['to']			# to of ith tx
    afrom = amount[i]['from']			# from of ith tx
    if i > 0:
      afrom1 = amount[i-1]['from']		# from of (i-1)th tx
    if afrom == '0x0000000000000000000000000000000000000000':  # if from 0x0 (minting)
      ts = ts + vi  # Minting increases total supply
    elif ato == '0x0000000000000000000000000000000000000000':  # if to 0x0 (recasting)
      ts = ts - vi  # Recasting decreases total supply
    elif ato == '0x26cab6888d95cf4a1b32bd37d4091aa0e29e7f68':  # recast fee collector
      pass
    elif ato == '0x00a55973720245819ec59c716b7537dac5ed4617':  # tx fee collector
      tx = tx + vi
      #elif amount[i]['to'] == '0x964f35fae36d75b1e72770e244f6595b68508cf5':  # kyber contract 
      #print('kyber')
    elif afrom == '0xd5be9efcc0fbea9b68fa8d1af641162bc92e83f2':  #  from digix marketplace
      vdigix = vdigix + vi
      wv = wv + vi                              # accumulate normal weekly volume
      tv = tv + vi                              # accumulate total volume
      '''
      When e.g. 10 DGX is sent 3 tx occur: first 0.013 (the tx fee), then 9.987, lastly 10. 
      This conditional avoids counting the 9.987 because the 0.013 and the 9.987 have the same 'from' address.
      '''
    elif afrom == afrom1:
      continue
    else:					# else is a normal tx
      wv = wv + vi                              # accumulate normal weekly volume
      tv = tv + vi                              # accumulate total volume
    if dt > cw*week:                            # if dt > cw weeks
      cw += 1                                   # +1 week
      y1 = round(float(wv)/1e9,2)                # round
      print(str(di.strftime("%d/%m/%Y")) + "|" + str(y1))  # print information
      y2 = round(float(ts)/1e9,2)
      y3 = round(float(vdigix)/1e9,2)
      f.write(str(di) + ' ' + str(y1) + ' ' + str(y3) + ' ' + str(y2) + '\n')    # write week number, volume to file
      di = d0 + datetime.timedelta(seconds=dt)  # datetime of ith tx
      wv = 0                                    # reset weekly volume 
      vdigix = 0                                # reset
  y1 = round(float(wv)/1e9,2)                	# round
  y2 = round(float(ts)/1e9,2)
  y3 = round(float(vdigix)/1e9,2)
  f.write(str(di) + ' ' + str(y1) + ' ' + str(y3) + ' ' + str(y2) + '\n')    # write week number, volume to file
print(str(di.strftime("%d/%m/%Y")) + "|" + str(y1))

# All-time volume table
#print("Current Quarter |" + str(dateq.strftime("%d/%m/%Y")) + "|" + str(qv) )
print("\n")
print("### All-time volume\n")
print("| All-time volume (DGX) |")
print("| --- |")
tv = round(float(tv)/1e9,2)
print("|" + str(tv) + "|\n")

print("### Total transaction fees collected\n")
print("| Transaction fees (DGX) |")
print("| --- |")
tx = round(float(tx)/1e9,2)                     # current, unfinished week
print("|" + str(tx) + "|\n")

print("### Total Supply\n")
print("| DGX Total Supply |")
print("| --- |")
ts = round(float(ts)/1e9,2)
print("|" + str(ts) + "|\n")

def dv():
  '''
  dv: writes datetime and daily volume to 'daily.dat' file
  '''
  
  dv = 0                                        # daily volume 
  tv = 0                                        # total volume
  cd = 1                                        # day counter (start at 1)
  ts = 0				       	# total supply
  di = d0 					# start on d0
  vdigix = 0

  with open('daily.dat','w+') as f:		# open file for writing
    for i in range(0,length):
      vi = int(amount[i]['value'])                # volume of ith tx
      ti = int(amount[i]['timeStamp'])	        # time of ith tx
      dt = ti - t0	                        # seconds since t0
      ato = amount[i]['to']			# to of ith tx
      afrom = amount[i]['from']			# from of ith tx
      if i > 0:
        afrom1 = amount[i-1]['from']		# from of (i-1)th tx
      if afrom == '0x0000000000000000000000000000000000000000':  # if from 0x0 (minting)
        ts = ts + vi  # Minting increases total supply
      elif afrom == '0xd5be9efcc0fbea9b68fa8d1af641162bc92e83f2':  #  from digix marketplace
        pass
      elif ato == '0x0000000000000000000000000000000000000000':  # if to 0x0 (recasting)
        ts = ts - vi  # Recasting decreases total supply
      elif ato == '0x26cab6888d95cf4a1b32bd37d4091aa0e29e7f68':  # recast fee collector
        pass
      elif afrom == '0xd5be9efcc0fbea9b68fa8d1af641162bc92e83f2':  #  from digix marketplace
        vdigix = vdigix + vi
        dv = dv + vi                            # accumulate weekly volume
      elif ato == '0x00a55973720245819ec59c716b7537dac5ed4617':  # tx fee collector
        pass
        #elif amount[i]['to'] == '0x964f35fae36d75b1e72770e244f6595b68508cf5':  # kyber contract 
        #print('kyber')
        '''
        When e.g. 10 DGX is sent 3 tx occur: first 0.013 (the tx fee), then 9.987, lastly 10. 
        This conditional avoids counting the 9.987 because the 0.013 and the 9.987 have the same 'from' address.
        '''
      elif afrom == afrom1:
        continue
      else:					# else is a normal tx
        dv = dv + vi                            # accumulate weekly volume
      if dt > cd*day:                           # if dt > cd days
        cd = int(dt/day) + 1                    # amount of days passed
        y1 = round(float(dv)/1e9,2)             # round
        y2 = round(float(ts)/1e9,2)
        y3 = round(float(vdigix)/1e9,2)
        f.write(str(di) + ' ' + str(y1) + ' ' + str(y3) + ' ' + str(y2) + '\n')    # write week number, volume to file
        di = d0 + datetime.timedelta(seconds=dt)  # datetime of ith tx
        dv = 0                                    # reset weekly volume 
    y1 = round(float(y1)/1e9,2)                   # current, unfinished week
    y2 = round(float(ts)/1e9,2)
    y3 = round(float(vdigix)/1e9,2)
    f.write(str(di) + ' ' + str(y1) + ' ' + str(y3) + ' ' + str(y2) + '\n')    # write week number, volume to file

  return

dv()
