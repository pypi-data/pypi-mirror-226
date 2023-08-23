"""Crypto exchange indicator application"""

import talib
import numpy

from .api.client import Client
from .exceptions import InvalidExchangeError

class CandleBoy:
    def __init__(self, exchange: str, verbose: bool = False):
        self._verbose = verbose
        self._exchange = exchange

        self._log(f'Connecting to {exchange}', ",")
        try:
            # Retrieve exchange proxy
            cli = Client()
            self._client = cli.connect(exchange, verbose)
        except InvalidExchangeError as e:
            print(e)
            print(f"\nExchanges supported {Client.exchanges()}")
        except Exception as e:
            print(f"Failed to connect to {exchange}: {e}")
        finally:
            self._log('done.')

    def _log(self, msg: str, end: str = None):
        """Print message to output if not silent

        Args:
            msg (str): Message to print to output
            end (str): String appended after the last value. Default a newline.
        """
        if self._verbose:
            print(msg, end=end)

# ---------------------------------- Getters --------------------------------- #

    @property
    def exchange(self):
        """Getter for exchange property

        Returns:
            Str: Current exchange
        """
        return self._exchange

# ------------------------------ Utility Methods ----------------------------- #

    def symbol(self, base: str, quote: str, code: str):
        """Creates a symbol representing the asset pairing

        Args:
            base (str): Currency you are buying (ex. 'btc')
            quote (str): Currency you are selling (ex. 'usd')
            code (str): Market code (ex. 'spot' or 'future')

        Returns:
            String: Formatted base and quote currency symbol
        """
        symbol = ""

        self._log(f'Creating symbol...{base}, {quote}, {code}', ',')
        try:
            symbol = self._client.symbol(base, quote, code)
        except Exception as e:
            print(f"Failed to create symbol...{base}, {quote}, {code}: {e}")
        finally:
            self._log('done.')

        return symbol

    def timeframes(self):
        """Retrieve all timeframes available for exchange

        Returns:
            List: All timeframes available
        """
        tfs = []

        self._log(f'Retrieving time frames from {self._exchange}', ",")
        try:
            tfs = self._client.timeframes()
        except Exception as e:
            print(f"Failed to retrieve time frames from {self._exchange}: {e}")
        finally:
            self._log('done.')

        return tfs

    def ohlcv(self, symbol: str, tf: str, since: str = None):
        """Retrieve the open - high - low - close - volume data from exchange

        Args:
            symbol (str): Pairing to retrieve OHLCV data for
            tf (str): Timeframe for OHLCV data
            since (str, optional): Optional start date for retrieving OHLCV data. Format as YEAR-MONTH-DAY (ex. 2018-12-01). Defaults to None.

        Returns:
            Tuple: open - high - low - close - volume data
        """
        timestamps = []
        open = []
        high = []
        low = []
        close = []
        volume = []
        candles = []

        self._log(f'Retrieving ohlcv data from {self._exchange}', ',')
        try:
            candles = self._client.ohlcv(symbol, tf, since)
        except Exception as e:
            print(f"Failed to retrieve ohlcv data from {self._exchange}: {e}")
        finally:
            # First value is timestamp
            # Then the following values are:
            # Open, High, Low, Close, Volume
            for candle in candles:
                timestamps.append(candle[0])
                open.append(candle[1])
                high.append(candle[2])
                low.append(candle[3])
                close.append(candle[4])
                volume.append(candle[5])
            self._log('done.')

        return timestamps, open, high, low, close, volume

# ------------------------------ Client Methods ------------------------------ #

    def verbose(self):
        """Turn on logging"""
        self._verbose = True

    def silent(self):
        """Turn off logging"""
        self._verbose = False

    def macd(self, close: list, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        """Returns the Moving Average Convergence/Divergence indicator values

        See TA-Lib docs for details on parameters.
        https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
        """
        # Format
        close = numpy.array(close, dtype=float)

        # Get indicator values
        macd, macdsignal, macdhist = talib.MACD(
            close, fastperiod, slowperiod, signalperiod)

        return macd, macdsignal, macdhist

    def ema(self, close: list, timeperiod: int = 200):
        """Returns the Exponential Moving Average indicator values

        See TA-Lib docs for details on parameters.
        https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
        """
        # Format
        close = numpy.array(close, dtype=float)

        # Get indicator values
        real = talib.EMA(close, timeperiod)

        return real
