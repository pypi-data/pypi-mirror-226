"""Tests the CandleBoy Module"""

import unittest

from candleboy.core import CandleBoy

class TestCore(unittest.TestCase):
    def test_init(self):
        candle = CandleBoy(exchange='phemex', verbose=True)
        self.assertEqual(isinstance(candle, CandleBoy), True)
        self.assertEqual(candle.exchange, 'phemex')

    def test_utility(self):
        candle = CandleBoy('phemex', True)

        tfs = candle.timeframes()
        self.assertEqual('1m' in tfs, True)

        symbol = candle.symbol(base='BTC', quote='USD', code='future')
        self.assertEqual(symbol, 'BTC/USD:USD')

        ohlcv = candle.ohlcv(symbol=symbol, tf='1m')
        self.assertGreater(len(ohlcv), 0)

        ohlcv = candle.ohlcv(symbol=symbol, tf='5m', since='2021-12-29')
        self.assertGreater(len(ohlcv), 0)

    def test_client(self):
        candle = CandleBoy('phemex', True)
        symbol = candle.symbol(base='BTC', quote='USD', code='future')
        tf = '1m'

        _, _, _, _, close, _ = candle.ohlcv(symbol, '1m')
        macd, _, _ = candle.macd(close)
        self.assertGreater(len(list(macd)), 0)

        ema = candle.ema(close)
        self.assertGreater(len(list(ema)), 0)
