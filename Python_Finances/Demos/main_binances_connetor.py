import os
from binance.client import Client
from dotenv import load_dotenv

# Cargamos variables de entorno
load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

client = Client(API_KEY, API_SECRET)

# Obtenemos el balance
account_info = client.get_account()

# Obtener el valor del Ticker BTCUSDT
ticker_btc = client.get_symbol_ticker(symbol='BTCUSDT')
print(f"Precio actual de BTC/USDT: {ticker_btc['price']}")

# Obtenemos los precios actuales (ticker price)
prices = {p['symbol']: float(p['price']) for p in client.get_all_tickers()}

print("Balances mayores a 1 USD:")
for balance in account_info['balances']:
    asset = balance['asset']
    free = float(balance['free'])
    locked = float(balance['locked'])
    total = free + locked

    if total == 0:
        continue

    # Calculamos el precio en USDT
    if asset == 'USDT':
        value_usd = total
    else:
        symbol = asset + 'USDT'
        price = prices.get(symbol)
        if price:
            value_usd = total * price
        else:
            # Si no hay par directo contra USDT lo saltamos
            continue

    if value_usd >= 1:
        print(f"{asset}: Total={total}, USD={value_usd:.2f}")
