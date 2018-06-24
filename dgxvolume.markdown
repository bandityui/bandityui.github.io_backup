---
layout: post
title:  "DGX Volume"
date:   2018-06-23 15:56:31 +0100
categories: DGX
---

```vega-lite
{
  "data": {
    "values": [
      {"a": "C", "b": 2}, {"a": "C", "b": 7}, {"a": "C", "b": 4},
      {"a": "D", "b": 1}, {"a": "D", "b": 2}, {"a": "D", "b": 6},
      {"a": "E", "b": 8}, {"a": "E", "b": 4}, {"a": "E", "b": 7}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {"field": "a", "type": "nominal"},
    "y": {"aggregate": "average", "field": "b", "type": "quantitative"}
  }
}
```



Current block: 5841427

Avg. block time of latest 5000 blocks: 14.4


DGX total supply (etherscan) = 50300

Total ETH in DAO contract address (etherscan) = 466648

DGX 24hr on-chain volume (last 54 transactions) = 1647.411748135

