from coca_websocket import WSConnector
import json, asyncio

CHANNELS = [
    "btc_jpy",
    "etc_jpy",
    "lsk_jpy",
    "mona_jpy",
    "plt_jpy",
    "fnct_jpy",
    "dai_jpy",
]


class Connector(WSConnector):
    def onRecieve(self, msg):
        items = [
            "timestamp",
            "tradeID",
            "pair",
            "rate",
            "volume",
            "method",
            "takerID",
            "makerID",
        ]
        insert_items = []
        print(type(msg))
        # for data in msg:
        # print(data)
        # item = dict(zip(items, data))

    def onError(self, error):
        print(type(error))


connector = Connector(
    "wss://ws-api.coincheck.com/",
    [
        {"type": "subscribe", "channel": f"{channel}-trades"}
        for channel in CHANNELS
    ],
)


def main():
    pass


try:
    # main()
    asyncio.run(connector.run())
except:
    pass
    # notifyLine("END")
