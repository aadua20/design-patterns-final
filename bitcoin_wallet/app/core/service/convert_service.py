from typing import Protocol

import requests


class IConvertor(Protocol):
    def btc_to_usd(self, btc: float) -> float:
        pass


class CoingateConvertService(IConvertor):
    url: str = "https://api.coingate.com/v2/rates/merchant/BTC/USD"

    def btc_to_usd(self, btc: float) -> float:
        data = requests.get(CoingateConvertService.url).text
        rate: float = float(data)
        return rate * btc
