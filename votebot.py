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
 wallet_user           = ''
 wallet_pass           = ''
 # Websocket URL to the full node
 witness_url           = "ws://127.0.0.1:7070"
 wallet_user           = ""
 wallet_password       = ""


client = SteemClient(Config)

# Account to vote as
whales = [] # Account to vote as

#Projects (Accounts, users, etc.) to follow
follow = []

#Get posts of those we follow:

startFrom = -1
limit = 20

while True:
  for account in follow:
    transactions = client.rpc.get_account_history(account,startFrom,limit)
    for transaction in transactions:
      if transaction[1]['op'][0] == "vote" and transaction[1]['op'][1]['voter'] == account:
        print("\nFound %s voted on [%s]" % (account, transaction[1]['op'][1]['permlink']))
  
        vt = transaction[1]['timestamp']
        ht = client.rpc.info()['time'] 
  
        vT = datetime.datetime(int(float(vt[0:-15])), int(float(vt[5:-12])), int(float(vt[8:10])), int(float(vt[11:-6])), int(float(vt[14:-3])), int(float(vt[17:])))
        hT = datetime.datetime(int(float(ht[0:-15])), int(float(ht[5:-12])), int(float(ht[8:10])), int(float(ht[11:-6])), int(float(ht[14:-3])), int(float(ht[17:])))
        age = (hT - vT) / timedelta(hours=1)

        if age < 24 and age > 0.25:
          for whale in whales:
            print("  Checking [%s] for missing votes..." % whale)
            whale_trans = client.rpc.get_account_history(whale,startFrom,500)
            voted = 0
  
            for wtrans in whale_trans:
              if wtrans[1]['op'][0] == "vote" and wtrans[1]['op'][1]['voter'] == whale:
                if wtrans[1]['op'][1]['permlink'] == transaction[1]['op'][1]['permlink']:
                  print("    Vote Found - skipping")
                  voted = 1;
  
            if voted == 0:
              try:
                client.rpc.vote(whale, transaction[1]['op'][1]['author'], transaction[1]['op'][1]['permlink'],100,'true')
                print("    Voting: %0.2f %s %s" % (age, whale, transaction[1]['op'][1]['permlink']))
              except:
                print("    Voting: %0.2f %s %s [FAILED]" % (age, whale, transaction[1]['op'][1]['permlink']))
        else: 
          print("      Post is too old - skipping")
  time.sleep(30)  
