#!/usr/bin/env python

from ib_trader import IBTrader
import time

import argparse


client_id = 1

if __name__ == "__main__":
    ibTrader = IBTrader(client_id, 4001)
    ibTrader.connect()
    ibTrader.place_simple_buy_order('AMZN', 1, 200)
    time.sleep(10)
    ibTrader.disconnect()
