from talib import EMA, RSI, MACD, ADX
import matplotlib.pyplot as plt
import numpy as np

class Indicators:

    def __init__(self, data):
        self.data = data
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
        
    def adx(self, timeperiod: int = 14):
        adx_values = ADX(self.high, self.low, self.close, timeperiod)
        return adx_values.dropna()
    
    def macd_lazybear(self):
        length = 20 
        mult = 2.0
        length_KC = 20
        mult_KC = 1.0

        # Calcule Bolliger Bands
        m_avg = self.close.rolling(window=length).mean()
        m_std = self.close.rolling(window=length).std(ddof=0) * mult_KC
        self.data['upper_BB'] = m_avg + m_std
        self.data['lower_BB'] = m_avg - m_std

        # Calcule True Range
        self.data['tr0'] = abs(self.high - self.low)
        self.data['tr1'] = abs(self.high - self.close.shift())
        self.data['tr2'] = abs(self.low - self.close.shift())
        self.data['tr'] = self.data[['tr0', 'tr1', 'tr2']].max(axis=1)
        
        # Calcule Keltner Channel
        range_ma = self.data['tr'].rolling(window=length_KC).mean()   
        self.data['upper_KC'] = m_avg + range_ma * mult_KC     
        self.data['lower_KC'] = m_avg - range_ma * mult_KC

        # Final Calcule 
        highest = self.high.rolling(window=length_KC).max()
        lowest = self.low.rolling(window=length_KC).min()
        m1 = (highest + lowest) / 2
        self.data['SQZ'] = self.close - (m1 + m_avg) / 2
        y = np.array(range(0, length_KC))
        func = lambda x: np.polyfit(y, x, 1)[0] * (length_KC - 1) + np. polyfit(y, x, 1)[1]
        self.data['SQZ'] = self.data['SQZ'].rolling(window=length_KC).apply(func, raw=True)

        return self.data

    def graph_layybear(self):
        df = self.macd_lazybear()

        fig = plt.figure(figsize=(14, 7))
        df['SQZ'].plot(label='lazybear', color='blue')
        plt.axhline(y=0, color='r', lw=0.5, ls='--')
        plt.legend(loc='best')

        plt.grid(linestyle='-.')
        plt.show()
        plt.close(fig)
    
    def graph_adx(self):
        adx = self.adx()

        fig = plt.figure(figsize=(14, 7))
        adx.plot(label='ADX', color='black')
        plt.axhline(y=23, color='r', lw=0.5, ls='--')
        plt.legend(loc='best')

        plt.grid(linestyle='-.')
        plt.show()
        plt.close(fig)

    def trading_latino(self):
        return self.ema(10), self.ema(55), self.adx(), self.macd_lazybear()