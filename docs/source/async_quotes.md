# 异步获取行情

### AsyncSinaQuote/AsyncTencentQuote

```py
import fastquotes
import asyncio

# quote = fastquotes.AsyncTencentQuote()
quote = fastquotes.AsyncSinaQuote()
codes = fastquotes.exchange_stock_list()

async def run():
    tick_dict = await quote.tick_dict(codes)
    print(len(tick_dict))
    print(tick_dict["000001"])

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
```

输出结果:

```
4072
{'time': '150003', 'name': '平安银行', 'code': '000001', 'current_price': 17.18, 'pre_close': 17.66, 'open': 17.42, 'high': 17.47, 'low': 16.69, 'total_amount': 2191492021.21, 'total_vol': 128918923.0, 'bid1_vol': 54800, 'bid1': 17.17, 'bid2_vol': 50600, 'bid2': 17.16, 'bid3_vol': 27749, 'bid3': 17.15, 'bid4_vol': 62300, 'bid4': 17.14, 'bid5_vol': 41300, 'bid5': 17.13, 'ask1_vol': 125226, 'ask1': 17.18, 'ask2_vol': 346501, 'ask2': 17.19, 'ask3_vol': 27749, 'ask3': 17.2, 'ask4_vol': 62300, 'ask4': 17.21, 'ask5_vol': 69300, 'ask5': 17.22}
```
