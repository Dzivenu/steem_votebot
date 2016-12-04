#!/usr/bin/python3
from steemapi.steemclient import SteemClient
import datetime
from datetime import timedelta,tzinfo
import yaml
import time
import os
import json
import sys

with open("config.yml", "r") as config_file:
  config = yaml.load(config_file)
  path   = config['path']
  pwFile = open(config['pw_file'], 'r')
  voters = config['voters']
  follow = config['follow']
  minPow = config['min_power']
  minAge = config['min_age']
  maxAge = config['max_age']

class Config():
 # Port and host of the RPC-HTTP-Endpoint of the wallet
 wallet_host           = "127.0.0.1"
 wallet_port           = 8091
 # Websocket URL to the full node
 witness_url           = "ws://127.0.0.1:7070"

client = SteemClient(Config)

pw = pwFile.readline()
pw = pw.rstrip()

#Get posts of those we follow:

startFrom = -1
limit = 2000


prev_power = 0

while True:
  for account in follow:
    voter = voters[len(voters)-1]
    voting_power = float(client.rpc.get_account(voter)['voting_power'])
    if voting_power < minPow:
      if prev_power != voting_power:
        print("Only at %0.2f%% - we need moar powa!!" % (voting_power/100))
      time.sleep(10)
      prev_power=voting_power 
      break
   
    prev_power = voting_power

    file_name = str(path + account + "_account_history.db")
    transactions = []
    with open( file_name, "r" ) as f:
      for line in f:
        try:
          transactions.append(json.loads(line))
        except:
          print("Could not append transaction: %s" % line)
    transactions = transactions[-100:]
    for transaction in transactions:
      if transaction[1]['op'][0] == "vote" and transaction[1]['op'][1]['voter'] == account and (transaction[1]['op'][1]['permlink'][0:3] != 're-' and transaction[1]['op'][1]['permlink'][-1:] != 'z'):
        #print("\nFound %s voted on [%s]" % (account, transaction[1]['op'][1]['permlink']))
        vt = transaction[1]['timestamp']
        ht = client.rpc.info()['time'] 
  
        vT = datetime.datetime(int(float(vt[0:-15])), int(float(vt[5:-12])), int(float(vt[8:10])), int(float(vt[11:-6])), int(float(vt[14:-3])), int(float(vt[17:])))
        hT = datetime.datetime(int(float(ht[0:-15])), int(float(ht[5:-12])), int(float(ht[8:10])), int(float(ht[11:-6])), int(float(ht[14:-3])), int(float(ht[17:])))
        age = (hT - vT) / timedelta(hours=1)

        for voter in voters:
          voting_power = float(client.rpc.get_account(voter)['voting_power'])

          if (age < maxAge) and (age > minAge) and (voting_power > minPow):
            try:
              client.rpc.unlock(pw)
              client.rpc.vote(voter, transaction[1]['op'][1]['author'], transaction[1]['op'][1]['permlink'],100.00,'true')
              client.rpc.lock()
              print("    Voting: %-1.2f %s %s %s " % (age, account, voter, transaction[1]['op'][1]['permlink']))
            except:
              client.rpc.lock()
              pass
