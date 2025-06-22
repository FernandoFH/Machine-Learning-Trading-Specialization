import os
from binance.spot import Spot
from pprint import pprint
from dotenv import load_dotenv

# Cargamos variables de entorno
load_dotenv()

class RobotBinances:
    """
    Bot para binances que permite la compra y venta del mercado SPOT 
    """
    __API_KEY = os.getenv('BINANCE_API_KEY')
    __API_SECRET = os.getenv('BINANCE_API_SECRET')

    def __init__(self, pair: str, temporality: str):
        """
        Inicializa el bot con el par de criptomonedas.
        
        :param pair: Par de criptomonedas a operar (ejemplo: 'BTCUSDT').
        :param temporality: Temporalidad de las velas (ejemplo: '1m', '5m', '15m', '1h', '4h').
        """
        self.pair = pair.upper()
        self.temporality = temporality
        self.symbol = self.pair.removesuffix("USDT")  # Extrae el símbolo de la criptomoneda sin 'USDT'

    def binace_client(self):
        """
        Inicioa el cliente de Binance para operar en el mercado SPOT.
        
        :return: Spot.
        """
        return Spot(api_key=self.__API_KEY, api_secret=self.__API_SECRET)
    
    def binance_account(self) -> dict:
        """
        Obtiene la información de la cuenta de Binance.
        
        :return: Información de la cuenta.
        """
        return self.binace_client().account()
    
    def cryptourrencies(self) -> list[dict]:
        """
        Obtiene la lista de criptomonedas con saldo positivo.
        
        :return: Lista de criptomonedas.
        """
        return [crypto for crypto in self.binance_account().get('balances') if float(crypto.get('free', 0)) > 0 or float(crypto.get('locked', 0)) > 0]

    def symbol_price(self, pair: str = "BTCUSDT") -> float:
        """
        Obtiene el precio actual de un par.
        
        :param pair: Par de la criptomoneda (ejemplo: 'BTCUSDT').
        :return: Precio del par.
        """
        return float(self.binace_client().ticker_price(pair.upper()).get('price'))

# Ejemplo de uso del bot
bot = RobotBinances(pair='BTCUSDT1`', temporality='4h')
pprint(bot.symbol_price())  

# print(bot.pair)  # Imprime el par de criptomonedas
    