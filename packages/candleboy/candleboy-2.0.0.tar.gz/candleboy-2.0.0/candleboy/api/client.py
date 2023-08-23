"""Connects to exchange clients"""

from phemexboy.proxy import Proxy
from candleboy.exceptions import InvalidExchangeError

class Client:
  def __init__(self):
    self._clients = {'phemex': Proxy}

  @classmethod
  def exchanges(self):
    """Returns a list of available exchanges

    Returns:
        List: Available exchanges
    """
    return ['phemex']

  def connect(self, exchange: str, verbose: bool = False):
    """Connect to exchange

    Args:
        exchange (str): Name of exchange
        verbose (bool, optional): Turn on logging. Defaults to False.

    Raises:
        InvalidExchangeError: Exchange not supported

    Returns:
        Object: Exchange proxy
    """
    if exchange not in Client.exchanges():
      raise InvalidExchangeError("Exchange not supported")

    return self._clients[exchange](verbose)


