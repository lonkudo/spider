import requests
import pandas as pd
from datetime import datetime

TRONGRID = "https://api.trongrid.io"

def get_fee(txid):
    try:
        url = f"{TRONGRID}/v1/transactions/{txid}"
        r = requests.get(url)
        data = r.json().get("data", [{}])[0]

        fee = data.get("cost", {}).get("net_fee", 0)
        return float(fee) / 1_000_000
    except:
        return None


def get_trc20_usdt_history(address, limit=20):
    url = f"{TRONGRID}/v1/accounts/{address}/transactions/trc20"
    params = {
        "limit": limit,
        "only_confirmed": "true"
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    data = r.json().get("data", [])

    rows = []

    for tx in data:
        if tx.get("token_info", {}).get("symbol") != "USDT":
            continue

        from_addr = tx.get("from")
        to_addr = tx.get("to")
        txid = tx.get("transaction_id")

        amount = float(tx.get("value", 0)) / 1_000_000

        if to_addr == address:
            tx_type = "IN"
        else:
            tx_type = "OUT"

        time = datetime.fromtimestamp(
            tx.get("block_timestamp", 0) / 1000
        )

        fee = get_fee(txid)

        rows.append({
            "txid": txid,
            "from": from_addr,
            "to": to_addr,
            "amount_usdt": amount,
            "type": tx_type,
            "gas_fee_trx": fee,
            "time": time
        })

    df = pd.DataFrame(rows)
    return df


# ---- usage ----
addr = "TVX8XueJcLMRj4iNKgmugXsRiHdp492C7f"

df = get_trc20_usdt_history(addr)

print(df)