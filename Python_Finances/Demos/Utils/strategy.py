from talib import EMA, RSI, MACD


class Indicators:

    def __init__(self, data):
        self.close = data.get('Close')
        self.open = data.get('Open')
        self.high = data.get('High')
        self.low = data.get('Low')

    def ema(self, timeperiod: int = 15):
        return float(EMA(self.close, timeperiod).iloc[-1])  # Retorna el último valor del EMA calculado
    
    def rsi(self, timeperiod: int = 15):
        return float(RSI(self.close, timeperiod).iloc[-1])  # Retorna el último valor del RSI calculado
    
    def macd(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        _macd, macdsignal, _ = MACD(self.close,  fastperiod,  slowperiod,  signalperiod)
        return tuple(map(float, (_macd.iloc[-1], macdsignal.iloc[-1])))