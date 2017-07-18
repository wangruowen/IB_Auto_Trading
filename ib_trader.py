# Learned from
# https://pythonprogramming.net/ibpy-tutorial-using-interactive-brokers-api-python/

from ib.opt import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from logger import logger


class IBTrader(object):
    def __init__(self, client_id, port):
        self.client_id = client_id
        self.port = port
        self.conn = Connection.create(port=port, clientId=client_id)
        self.is_connected = False
        self.order_history = {}  # order_id -> order, contract
        self.current_order_id = 0

    def connect(self):
        self.is_connected = self.conn.connect()

    def disconnect(self):
        self.conn.disconnect()

    def make_contract(self, symbol, sec_type, exch, prim_exch, curr):
        if not self.is_connected:
            logger.error("IB is not connected! Please connect to IB first.")
            return None

        Contract.m_symbol = symbol
        Contract.m_secType = sec_type
        Contract.m_exchange = exch
        Contract.m_primaryExch = prim_exch
        Contract.m_currency = curr
        logger.info("Make Contract: %s %s %s %s %s", symbol, sec_type, exch, prim_exch, curr)

        return Contract

    def make_order(self, action, quantity, price=None):
        if not self.is_connected:
            logger.error("IB is not connected! Please connect to IB first.")
            return None

        if price is not None:
            order = Order()
            order.m_orderType = 'LMT'
            order.m_totalQuantity = quantity
            order.m_action = action
            order.m_lmtPrice = price
        else:
            order = Order()
            order.m_orderType = 'MKT'
            order.m_totalQuantity = quantity
            order.m_action = action
        logger.info("Make Order: %s %s with Quantity: %s at Price: %s",
                    order.m_action, order.m_orderType, order.m_totalQuantity, price)

        return order

    def create_simple_buy_order(self, symbol, quantity, price=None):
        if not self.is_connected:
            logger.error("IB is not connected! Please connect to IB first.")
            return None, None, None

        contract = self.make_contract(symbol, "STK", "SMART", "SMART", "USD")
        order = self.make_order("BUY", quantity, price)
        self.current_order_id += 1
        self.order_history[self.current_order_id] = (order, contract)
        logger.info("Create Simple BUY Order: %s with Quantity: %s at Price: %s", symbol, quantity, price)

        return self.current_order_id, contract, order

    def place_order(self, order_id, contract, order):
        if not self.is_connected:
            logger.error("IB is not connected! Please connect to IB first.")
            return None
        logger.info("Place Order: %s, %s with Quantity: %s at Price: %s",
                    order.m_action, contract.m_symbol, order.m_totalQuantity,
                    order.m_lmtPrice if order.m_orderType == 'LMT' else "MARKET PRICE")
        self.conn.placeOrder(order_id, contract, order)

    def place_simple_buy_order(self, symbol, quantity, price=None):
        if not self.is_connected:
            logger.error("IB is not connected! Please connect to IB first.")
            return None

        order_id, contract, order = self.create_simple_buy_order(symbol, quantity, price)
        if order_id is not None:
            self.place_order(order_id, contract, order)
