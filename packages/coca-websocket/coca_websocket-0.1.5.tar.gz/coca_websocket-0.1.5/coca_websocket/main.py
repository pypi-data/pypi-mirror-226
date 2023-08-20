from coca_websocket import WSConnector
import json


# class Test(WSConnector):
#     def onRecieve(self, msg):
#         return super().onRecieve(msg)

a = '[["1663318663","2357062","btc_jpy","2820896.0","5.0","sell","1193401","2078767"],["1663318892","2357068","btc_jpy","2820357.0","0.7828","buy","4456513","8046665"]]'
b = json.loads(a)

print(b[0])
