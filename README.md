# bandityui.github.io

### Tx format and counting correctly

To correctly count the volume of the DGX token, the tx format needs to be understood. Each DGX tx actually ends up as 3 txs, e.g. when 10 DGX is sent 3 tx occur: first 0.013 (the 0.13% tx fee), then 9.987, lastly 10; in that order on etherscan. The real volume of the tx is 10 and if we just added all the values of all the DGX txs we would double-count. To avoid this, note that the 0.013 fee and the 9.987 always have the same 'from' address. Therefore, we can include a conditional like,

```python
for i in range(0,len(a)):       # loop over all txs
  vi = int(a[i]['value'])       # volume of ith tx
  afrom = a[i]['from']          # from address of ith tx
  if i > 0:
    afrom1 = a[i-1]['from']     # from address of (i-1)th tx
  if afrom == afrom1:
    continue                    # go immediately to next loop iteration
  else:
    xv += vi                    # accumulate volume
```

### Important tx types

When DGX is minted the from address is the zero-address (0x0), and when DGX is recast (redeemed for real gold) it is sent to 0x0 and a 1% fee is sent to a specific address. It is useful to count the tx fees and the total supply of DGX. Thus, we can count these appropriately (or avoid counting them),

```python
for i in range(0,len(a)):       # loop over all txs
  vi = int(a[i]['value'])       # volume of ith tx
  ato = a[i]['to']              # to address of ith tx
  afrom = a[i]['from']          # from address of ith tx
  if i > 0:
    afrom1 = a[i-1]['from']     # from address of (i-1)th tx
  if afrom == '0x0000000000000000000000000000000000000000':     # if from 0x0 (minting)
    ts += vi                                             # Count DGX minted
  elif ato == '0x0000000000000000000000000000000000000000':     # if to 0x0 (recasting)
    ts -= vi                                             # Subtract if recasted
  elif ato == '0x26cab6888d95cf4a1b32bd37d4091aa0e29e7f68':     # recast fee collector
    pass                        # do nothing
  elif ato == '0x00a55973720245819ec59c716b7537dac5ed4617':     # tx fee collector
    tx += vi                    # count tx fees
  elif afrom == afrom1:
    continue                    # go immediately to next loop iteration
  else:
    xv += vi                    # accumulate volume
```

