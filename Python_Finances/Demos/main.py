import os
from binance.spot import Spot
from pprint import pprint
import pandas as pd
from dotenv import load_dotenv
from Utils.strategy import Indicators

# Cargamos variables de entorno
load_dotenv()

class RobotBinances:
    """
    Bot para binances que permite la compra y venta del mercado SPOT 
    """
    __API_KEY = os.getenv('BINANCE_API_KEY')
    __API_SECRET = os.getenv('BINANCE_API_SECRET')
    binace_client = Spot(api_key=__API_KEY, api_secret=__API_SECRET)

    def __init__(self, pair: str, temporality: str):
        """
        Inicializa el bot con el par de criptomonedas.
        
        :param pair: Par de criptomonedas a operar (ejemplo: 'BTCUSDT').
        :param temporality: Temporalidad de las velas (ejemplo: '1m', '5m', '15m', '1h', '4h').
        """
        self.pair = pair.upper()
        self.temporality = temporality
        self.symbol = self.pair.removesuffix("USDT")  # Extrae el símbolo de la criptomoneda sin 'USDT'

    def _request(self, endpoint: str, parameters: dict  = None):
        while True:
            try:
                response = getattr(self.binace_client, endpoint)
                return response() if parameters is None else response(**parameters)
            except Exception as e:
                pprint(f"Error en la solicitud a Binance: {e}, en el endpoint: {endpoint}, con parámetros: {parameters}")
                break
    
 
    def binance_account(self) -> dict:
        """
        Obtiene la información de la cuenta de Binance.
        
        :return: Información de la cuenta.
        """
        return self._request('account')
    
    def cryptourrencies(self) -> list[dict]:
        """
        Obtiene la lista de criptomonedas con saldo positivo.
        
        :return: Lista de criptomonedas.
        """
        return [crypto for crypto in self.binance_account().get('balances') if float(crypto.get('free', 0)) > 0 or float(crypto.get('locked', 0)) > 0]

    def symbol_price(self, pair: str = None) -> float:
        """
        Obtiene el precio actual de un par.
        
        :param pair: Par de la criptomoneda (ejemplo: 'BTCUSDT').
        :return: Precio del par.
        """
        symbol = self.pair if pair is None else pair
        return float(self._request('ticker_price', {'symbol': symbol.upper()}).get('price'))
    
    def candlesstick(self, limit: int = 50) -> pd.DataFrame:
        """
        Obtiene las velas del par de criptomonedas.
        
        :return: Lista de velas.
        """
        params = {
            'symbol': self.pair.upper(),
            'interval': self.temporality,
            'limit': limit
        }

        candel = pd.DataFrame(self._request('klines', params), 
                              columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume','Close time', 
                                       'Quote asset volume', 'Number of trades','Taker buy base asset volume', 
                                       'Taker buy quote asset volume', 'Ignore'], 
                                       dtype=float) 
        
        return candel[['Open time','Close time', 'Open', 'High', 'Low', 'Close', 'Volume']].astype(float)

    
# Ejemplo de uso del bot
bot = RobotBinances('BTCUSDT', '4h')
pprint(Indicators(bot.candlesstick()).macd())  # Imprime el EMA de las velas del par


# pprint(bot.candlesstick())  # Imprime el precio actual del par
# print(bot.pair)  # Imprime el par de criptomonedas
    