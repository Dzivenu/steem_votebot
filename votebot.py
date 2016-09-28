from steemapi.steemclient import SteemClient
import datetime
from datetime import timedelta,tzinfo
import time
import os
import json
import sys

class Config():
 # Port and host of the RPC-HTTP-Endpoint of the wallet
 wallet_host           = "127.0.0.1"
 wallet_port           = 8091
 wallet_user           = 'river'
 wallet_pass           = 'head'
 # Websocket URL to the full node
 witness_url           = "ws://127.0.0.1:7070"
 wallet_user           = ""
 wallet_password       = ""


client = SteemClient(Config)

# Accounts to vote with
whales = [""] 

#Accounts to vote as
follow = ["curie","positivity","littlekitty"]

#tags = ["project-positivity"]

#Get posts of those we follow:
startFrom = -1
limit = 100

#Vote on posts our tracked accounts vote on that are older than 15 minutes but newer than 24 hours.
while True:
  for account in follow:
    transactions = client.rpc.get_account_history(account,startFrom,limit)
    for transaction in transactions:
      if transaction[1]['op'][0] == "vote" and transaction[1]['op'][1]['voter'] == account:
  
        vt = transaction[1]['timestamp']
        ht = client.rpc.info()['time'] 
  
        vT = datetime.datetime(int(float(vt[0:-15])), int(float(vt[5:-12])), int(float(vt[8:10])), int(float(vt[11:-6])), int(float(vt[14:-3])), int(float(vt[17:])))
        hT = datetime.datetime(int(float(ht[0:-15])), int(float(ht[5:-12])), int(float(ht[8:10])), int(float(ht[11:-6])), int(float(ht[14:-3])), int(float(ht[17:])))
  
        for whale in whales:
          whale_trans = client.rpc.get_account_history(whale,startFrom,limit)
          voted = 0
  
          for wtrans in whale_trans:
            if wtrans[1]['op'][0] == "vote" and wtrans[1]['op'][1]['voter'] == whale:
              if wtrans[1]['op'][1]['permlink'] == transaction[1]['op'][1]['permlink']:
                voted = 1;
  
          if voted == 0:
            age = (hT - vT) / timedelta(hours=1)
            if age < 24 and age > 0.25:
              print("%0.2f %s %s" % (age, whale, transaction[1]['op'][1]['permlink']))
              client.rpc.vote(whale, transaction[1]['op'][1]['author'], transaction[1]['op'][1]['permlink'],100,'true')
  
  
