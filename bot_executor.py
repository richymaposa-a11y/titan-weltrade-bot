import sys
import argparse
from mt5linux import MetaTrader5 as mt5

parser = argparse.ArgumentParser()
parser.add_argument("--login", type=int, required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--server", required=True)
parser.add_argument("--symbol", default="EURUSD")
parser.add_argument("--lot", type=float, default=0.01)
args = parser.parse_args()

if not mt5.initialize(login=args.login, password=args.password, server=args.server):
    print(f"[ERROR] Weltrade MT5 Initialization failed: {mt5.last_error()}")
    mt5.shutdown()
    sys.exit(1)

print(f"[SUCCESS] Connected to Weltrade Account {args.login}")

symbol = args.symbol
lot = args.lot
price = mt5.symbol_info_tick(symbol).ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "deviation": 20,
    "magic": 999111,
    "comment": "Titan Weltrade Bot",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": 2,
}

result = mt5.order_send(request)
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"[ERROR] Trade execution failed with code: {result.retcode}")
else:
    print(f"[SUCCESS] Order opened on Weltrade! Ticket ID: {result.order}")

mt5.shutdown()
