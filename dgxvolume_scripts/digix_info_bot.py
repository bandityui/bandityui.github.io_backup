import urllib.request
import json
import datetime

now = datetime.datetime.now()
print("This page updates hourly using data from the [DGX contract address (etherscan)](https://etherscan.io/token/0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf). Last updated:")
print(now.strftime("%Y-%m-%d %H:%M") + ' UTC\n')

# Current block
with open('current.block') as f:
  a = f.read()
currentblock,blocktime = a.split(" ")
#print('Current block: ' + currentblock + '\n')
#print('Avg. block time of latest 5000 blocks: ' + blocktime + '\n')

# ETH held by DAO contract address
#with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=balance&address=0xF0160428a8552AC9bB7E050D90eEADE4DDD52843&tag=latest&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  #data = json.loads(url.read().decode())
#amount = data.get("result","None")
#msg = "Total ETH in DAO contract address (etherscan) = " + str(amount[:-18])
#print(msg + '\n')

# DGX on-chain volume
with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&page=1&offset=999999&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  data = json.loads(url.read().decode())
amount = data.get("result","None")
x = 0
length = len(amount)
# what is the block of the latest transaction?
#lastblock = amount[length-1]['blockNumber']
#lastts = amount[length-1]['timeStamp']
#print('Last block containing a DGX tx = ' + lastblock)
#print('Timestamp of last block containing a DGX tx = ' + lastts)
# find n = number of transactions within last ~24 hours
nblocks = int(3600*24/float(blocktime))
block1 = int(currentblock) - nblocks
#print('24 hrs ago block (block1) = ' + str(block1))
# loop backwards until block just higher than 'block1'
n = 0
for i in range(length,0,-1):
  block = amount[i-1]['blockNumber']
  ts = amount[i-1]['timeStamp']
  if int(block)>block1:
    ts2 = ts
    block2 = block
    n += 1
#print('Closest block to block1 with a DGX tx = ' + str(block2))
#print('Timestamp of closest block to block1 with a DGX tx = ' + str(ts2))
currentts = int(ts2) + 3600*24
#print('Approx. current timestamp = ' + str(currentts))
#print('How close to real 24hrs (= 1 is perfect): ' + str((int(lastts)-int(ts2))/(24*3600.)))
for i in range(length,length-n,-1):
  x = x + int(amount[i-1]['value'])
msg = "DGX 24hr on-chain volume (last " + str(n) + ' transactions) = ' + str(float(x)/1e9)
print(msg + '\n')
Jun24_2018_10am = 1529831840
f=open("24hr_volume.dat", "a+")
hrs_from_start = (currentts - Jun24_2018_10am)/3600
#f.write(str(hrs_from_start) + ' ' + str(float(x)/1e9) + '\n')
f.write(str(now.strftime("%Y-%m-%d %H:%M")) + ' ' + str(float(x)/1e9) + '\n')

# DGX total supply
with urllib.request.urlopen("https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  data = json.loads(url.read().decode())
amount = data.get("result","None")
msg = "###### DGX total supply (etherscan) = \n" + str(amount[:-9]) 
print(msg)

