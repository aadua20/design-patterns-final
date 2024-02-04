from typing import Protocol

import requests


class IConvertor(Protocol):
    def btc_to_usd(self, btc: float) -> float:
        pass

    def satoshi_to_btc(self, satoshi: int) -> float:
        pass


class ConvertService(IConvertor):
    URL: str = "https://api.coingate.com/v2/rates/merchant/BTC/USD"
    BTC_TO_SATOSHI = 100_000_000

    def btc_to_usd(self, btc: float) -> float:
        data = requests.get(self.URL).text
        rate: float = float(data)
        return rate * btc

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / self.BTC_TO_SATOSHI
