# Import necessary libraries
import talib as ta
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('bmh')

aapl = yf.download("AAPL", start="2019-01-01", end="2022-01-01", auto_adjust=True)

# Medias móviles simples
close = aapl['Close'].to_numpy().flatten()
aapl['SMA_20'] = ta.SMA(close, timeperiod=20)
aapl['EMA_50'] = ta.EMA(close, timeperiod=50)

# Grafica EMA Y SMA
plt.figure(figsize=(15, 15))
plt.plot(aapl['Close'], label='Precio de Cierre', color='blue')
plt.plot(aapl['SMA_20'], label='SMA 20', color='orange')
plt.plot(aapl['EMA_50'], label='EMA 50', color='green')
plt.title('AAPL Precio de Cierre con SMA y EMA')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid()
plt.show()

# Bollinger Bands
aapl['BB_upper'], aapl['BB_middle'], aapl['BB_lower'] = ta.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

plt.figure(figsize=(15, 8))

# Precio de cierre
plt.plot(aapl.index, aapl['Close'], label='Precio de Cierre', color='blue')

# Bollinger Bands
plt.plot(aapl.index, aapl['BB_upper'], label='Bollinger Upper', color='red', linestyle='--')
plt.plot(aapl.index, aapl['BB_middle'], label='Bollinger Middle (SMA 20)', color='orange')
plt.plot(aapl.index, aapl['BB_lower'], label='Bollinger Lower', color='green', linestyle='--')

plt.fill_between(aapl.index, aapl['BB_lower'], aapl['BB_upper'], color='grey', alpha=0.2)

plt.title('Bollinger Bands')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.grid()
plt.show()

### RSI
aapl['RSI'] = ta.RSI(close, timeperiod=14)
plt.figure(figsize=(15, 5))
plt.plot(aapl.index, aapl['RSI'], label='RSI', color='purple')
plt.axhline(70, color='red', linestyle='--', label='Sobrecompra (70)')
plt.axhline(30, color='green', linestyle='--', label='Sobreventa (30)')
plt.title('Índice de Fuerza Relativa (RSI) de AAPL')
plt.xlabel('Fecha')
plt.ylabel('RSI')
plt.legend()
plt.grid()
plt.show()