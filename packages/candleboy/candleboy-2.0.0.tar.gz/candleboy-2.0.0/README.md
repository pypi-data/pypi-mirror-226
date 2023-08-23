# CandleBoy
Crypto exchange indicator application

## Todo
- Add more indicators
- Add more exchanges

## Notes
- Only exchange is Phemex so far, they require specific symbols for SPOT and FUTURE
- SPOT Symbols start with *s* and are handled in USDT ex. sBTCUSDT
- FUTURE Symbols are all formatted as so *BTC/USD:USD*

## Installation
- Requires TA-Lib which may be difficult to install
- Here is their install docs https://mrjbq7.github.io/ta-lib/install.html

```
pip install candleboy
```

## Usage
### Instantiation
```
# Only exchange at the moment is phemex
# Verbose shows logging
client = CandleBoy(exchange='phemex', verbose=True)

# Turn logging on/off
client.verbose()
client.silent()

# Access current exchange property
print(client.exchange)
```

### Get a list of all available timeframes for an exchange
```
client.timeframes()
```

### Retrieve Open, High, Low, Close, Volume data from exchange
- Some exchanges may return different values
- Retrieves 1000 candles for phemex
```
# Create symbol first
symbol = client.symbol(base='BTC', quote='USD', code='future') # BTC/USD:USD

timestamps, open, high, low, close, volume = client.ohlcv(symbol=symbol, tf='1m')

# Use a start at date
date = '2021-12-29' # YEAR-MONTH-DATE
timestamps, open, high, low, close, volume = client.ohlcv(symbol=symbol, tf='1m', since=date)
```

### Get Moving Average Convergence/Divergence Indicator Values
```
symbol = client.symbol(base='BTC', quote='USD', code='future')
_, _, _, _, close, _ = client.ohlcv(symbol, '1m')
macd, signal, histogram = client.macd(close)

# May optionally change parameters (default is 12, 26, 9)
fastperiod=9
slowperiod=12
signalperiod=3

macd, signal, histogram = client.macd(close, fastperiod, slowperiod, signalperiod)
```

### Get Exponential Moving Average Indicator Values
```
symbol = client.symbol(base='BTC', quote='USD', code='future')
_, _, _, _, close, _ = client.ohlcv(symbol, '1m')
ema = client.ema(close)

# May optionally change parameters (default is 200)
timeperiod = 20

ema = client.ema(close, timeperiod)
```

## Test

- Runs the tests on the CandleBoy module

```
make test
```

or

```
python3 test
