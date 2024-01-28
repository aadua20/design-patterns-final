from typing import Protocol
from urllib.request import urlopen


class IConvertor(Protocol):
    def btc_to_usd(self, btc: float) -> float:
        pass


class CoingateConvertService(IConvertor):
    url: str = "https://api.coingate.com/v2/rates/merchant/BTC/USD"

    def btc_to_usd(self, btc: float) -> float:
        data = urlopen(CoingateConvertService.url).read().decode("utf-8")
        rate: float = float(data)
        return rate * btc
