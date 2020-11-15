import asyncio

import aiohttp

from fastquotes.const import HEADERS, REQ_CODES_NUM_MAX, TENCENT_BASE_URL
from fastquotes.utils import parse_out_tencent_tick_dict

from . import async_quote


class AsyncTencentQuote(async_quote.AsyncQuote):
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def tick_dict(self, codes: list) -> dict:
        res = {}
        tasks = []

        async def small_price_dict(codes: list):
            data_str = await self._fetch_data_str(codes)
            data_list = data_str.strip().split("\n")
            for item in data_list:
                tick_dict = parse_out_tencent_tick_dict(item)
                if tick_dict is None:
                    return
                res[tick_dict["code"]] = tick_dict

        codes_len = len(codes)
        for i in range(0, codes_len, REQ_CODES_NUM_MAX):
            if i + REQ_CODES_NUM_MAX >= codes_len:
                small_codes = codes[i:]
            else:
                small_codes = codes[i : i + REQ_CODES_NUM_MAX]
            tasks.append(small_price_dict(small_codes))
        await asyncio.wait(tasks)
        return res

    async def price_dict(self, codes: list) -> dict:
        res = {}
        tasks = []

        async def small_price_dict(codes: list):
            data_str = await self._fetch_data_str(codes)
            data_list = data_str.strip().split("\n")
            for item in data_list:
                s = item.split("~")
                try:
                    code, price = s[2], float(s[3])
                except IndexError:
                    continue
                res[code] = price

        codes_len = len(codes)
        for i in range(0, codes_len, REQ_CODES_NUM_MAX):
            if i + REQ_CODES_NUM_MAX >= codes_len:
                small_codes = codes[i:]
            else:
                small_codes = codes[i : i + REQ_CODES_NUM_MAX]
            tasks.append(small_price_dict(small_codes))
        await asyncio.wait(tasks)
        return res

    async def close(self):
        await self._session.close()

    async def _fetch_data_str(self, codes: str) -> str:
        codes_str = ",".join(codes)
        async with await self._session.get(
            f"{TENCENT_BASE_URL}{codes_str}", headers=HEADERS
        ) as response:
            return await response.text()