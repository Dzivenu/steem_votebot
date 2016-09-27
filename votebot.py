from steemapi.steemclient import SteemClient
import datetime
import time
import os
import json


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

# Account to vote as
whale = "riverhead" # Account to vote as

#Projects (Accounts, users, etc.) to follow
follow = ["curie","positivity"]
tags = ["project-positivity"]

#Get posts of those we follow:

startFrom = -1
limit = 500

whale_trans = client.rpc.get_account_history(whale,startFrom,limit)

for account in follow:
  transactions = client.rpc.get_account_history(account,startFrom,limit)
  for transaction in transactions:
    if transaction[1]['op'][0] == "vote" and transaction[1]['op'][1]['voter'] == account:
      voted = 0

      for wtrans in whale_trans:
        if wtrans[1]['op'][0] == "vote" and wtrans[1]['op'][1]['voter'] == whale:
          if wtrans[1]['op'][1]['permlink'] == transaction[1]['op'][1]['permlink']:
            voted = 1;

      if voted == 0:
        print("Voting on: %s" % (transaction[1]['op'][1]['permlink']))
        client.rpc.vote(whale, transaction[1]['op'][1]['author'], transaction[1]['op'][1]['permlink'],100,'true')

