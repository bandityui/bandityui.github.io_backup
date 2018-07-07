import urllib.request
import json
import datetime

def xvolume(x,printtable):
  '''
  xvolume: writes datetime and volume to .dat file every 'x' time-period (seconds) 
  '''
  
  xv = 0                                        # volume in time period 'x'
  vdigix = 0					# volume from digix marketplace
  tv = 0                                        # total volume
  tx = 0                                        # tx fees collected
  cx = 1                                        # count time periods (start at 1)
  ts = 0				       	# total supply
  di = d0 					# start on d0

  with open(str(x) + '.dat','w+') as f:		# open file for writing
    for i in range(0,length):
      vi = int(amount[i]['value'])              # volume of ith tx
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
        '''
        When e.g. 10 DGX is sent 3 tx occur: first 0.013 (the tx fee), then 9.987, lastly 10. 
        This conditional avoids counting the 9.987 because the 0.013 and the 9.987 have the same 'from' address.
        '''
      elif afrom == afrom1:
        continue
      #elif afrom == '0xd5be9efcc0fbea9b68fa8d1af641162bc92e83f2':  #  from digix marketplace
      #  vdigix = vdigix + vi			# accumulate volume from digix marketplace
      #  xv = xv + vi                            # accumulate 'x'ly volume
      #  tv = tv + vi                            # accumulate total volume
      else:					# else is a normal tx
        xv = xv + vi                            # accumulate 'x'ly volume
        tv = tv + vi                            # accumulate total volume
      if dt > cx*x:                             # if dt > cx multiples of x time periods
        cx = int(dt/x) + 1                      # amount of x time periods passed
        y1 = round(float(xv)/1e9,2)             # round
        if printtable == 1:
          print(str(di.strftime("%d/%m/%Y")) + "|" + str(y1))  # print information
        y2 = round(float(ts)/1e9,2)
        f.write(str(di) + ' ' + str(y1) + ' ' + str(y2) + '\n')    # write date, volume to file
        di = d0 + datetime.timedelta(seconds=dt)  # datetime of ith tx
        xv = 0                                    # reset x volume 
    xv = round(float(xv)/1e9,2)                   # current, unfinished week
    tv = round(float(tv)/1e9,2)
    ts = round(float(ts)/1e9,2)
    tx = round(float(tx)/1e9,2)
    vdigix = round(float(vdigix)/1e9,2)
    f.write(str(di) + ' ' + str(xv) + ' ' + str(ts) + '\n')    	   # write date, volume to file
  if printtable == 1:
    print(str(di.strftime("%d/%m/%Y")) + "|" + str(xv))
  
  return xv,tv,ts,tx


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

t0 = int(amount[0]['timeStamp'])	        # time (s) of first tx 
tlast = amount[length-1]['timeStamp']           # time (s) of last tx 
dt = int(tlast) - int(t0)			# time between 1st and last txs
d0 = now - datetime.timedelta(seconds=dt)	# current time minus dt
di = d0

# Begin weekly table
print("### Weekly volume table\n")
print("Week Starting | Volume (DGX)")
print("--- | ---")

wv,tv,ts,tx = xvolume(week,1)

# All-time volume table
#print("Current Quarter |" + str(dateq.strftime("%d/%m/%Y")) + "|" + str(qv) )
print("\n")
print("### All-time volume\n")
print("| All-time volume (DGX) |")
print("| --- |")
print("|" + str(tv) + "|\n")

print("### Total transaction fees collected\n")
print("| Transaction fees (DGX) |")
print("| --- |")
print("|" + str(tx) + "|\n")

print("### Total Supply\n")
print("| DGX Total Supply |")
print("| --- |")
print("|" + str(ts) + "|\n")

wv,tv,ts,tx = xvolume(day,0)

