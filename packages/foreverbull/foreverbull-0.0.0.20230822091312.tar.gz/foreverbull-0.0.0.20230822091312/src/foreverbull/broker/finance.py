from datetime import datetime
from typing import List

import requests

from .http import api_call


@api_call
def get_assets() -> requests.Request:
    return requests.Request(
        method="GET",
        url="/finance/api/assets",
        params={},
    )


@api_call
def add_assets(symbols: List[str]) -> requests.Request:
    return requests.Request(
        method="POST",
        url="/finance/api/assets",
        json={"symbols": symbols},
    )


@api_call
def check_ohlc(symbols: List[str], start: datetime, end: datetime) -> requests.Request:
    return requests.Request(
        method="HEAD",
        url="/finance/api/ohlc/check",
        params={"symbols": symbols, "startTime": start.isoformat(), "endTime": end.isoformat()},
    )


@api_call
def download_ohlc(symbols: List[str], start: datetime, end: datetime) -> requests.Request:
    return requests.Request(
        method="POST",
        url="/finance/api/ohlc",
        json={"symbols": symbols, "start_time": start.isoformat(), "end_time": end.isoformat()},
    )
