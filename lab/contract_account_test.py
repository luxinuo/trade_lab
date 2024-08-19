# coding: utf-8

import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import time
import hashlib
import hmac
import requests
import json

import ccxt
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
from datetime import datetime, timedelta

import os
from colorama import Fore, Back, Style, init


pd.options.mode.chained_assignment = None  # default='warn'


def gen_sign(method, url, query_string=None, payload_string=None):
    sign_path = "../cred/credentials.json"

    # Read the credentials from the file
    with open(sign_path, "r") as f:
        data = json.load(f)
        key = data["pub_key"]
        secret = data["secret_key"]

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode("utf-8"))
    hashed_payload = m.hexdigest()
    s = "%s\n%s\n%s\n%s\n%s" % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(
        secret.encode("utf-8"), s.encode("utf-8"), hashlib.sha512
    ).hexdigest()
    return {"KEY": key, "Timestamp": str(t), "SIGN": sign}


def get_data():
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # url = '/account/detail'
    url = "/wallet/total_balance"
    query_param = ""
    sign_headers = gen_sign("GET", prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request("GET", host + prefix + url, headers=headers)
    # print(r.json())
    return r.json()


def fetch_account_info_test():
    res = get_data()
    return {
        "details": {
            "delivery": {
                "currency": "USDT",
                "amount": res["details"]["delivery"]["amount"],
                "unrealised_pnl": res["details"]["delivery"]["unrealised_pnl"],
            },
            "finance": {
                "currency": "USDT",
                "amount": res["details"]["finance"]["amount"],
            },
            "futures": {
                "currency": "USDT",
                "amount": res["details"]["futures"]["amount"],
                "unrealised_pnl": res["details"]["futures"]["unrealised_pnl"],
            },
            "margin": {
                "currency": "USDT",
                "amount": res["details"]["margin"]["amount"],
                "borrowed": res["details"]["margin"]["borrowed"],
            },
            "options": {
                "currency": "USDT",
                "amount": res["details"]["options"]["amount"],
                "unrealised_pnl": res["details"]["options"]["unrealised_pnl"],
            },
            "payment": {
                "currency": "USDT",
                "amount": res["details"]["payment"]["amount"],
            },
            "quant": {"currency": "USDT", "amount": res["details"]["quant"]["amount"]},
            "spot": {"currency": "USDT", "amount": res["details"]["spot"]["amount"]},
        },
        "total": {
            "amount": res["total"]["amount"],
            "borrowed": res["total"]["borrowed"],
            "currency": res["total"]["currency"],
            "unrealised_pnl": res["total"]["unrealised_pnl"],
        },
    }


# Mock-up function for fetching data - replace this with your actual fetching logic
def fetch_account_info():
    res = get_data()
    return {
        "details": {
            "delivery": {
                "currency": "USDT",
                "amount": res["details"]["delivery"]["amount"],
                "unrealised_pnl": res["details"]["delivery"]["unrealised_pnl"],
            },
            "finance": {
                "currency": "USDT",
                "amount": res["details"]["finance"]["amount"],
            },
            "futures": {
                "currency": "USDT",
                "amount": res["details"]["futures"]["amount"],
                "unrealised_pnl": res["details"]["futures"]["unrealised_pnl"],
            },
            "margin": {
                "currency": "USDT",
                "amount": res["details"]["margin"]["amount"],
                "borrowed": res["details"]["margin"]["borrowed"],
            },
            "options": {
                "currency": "USDT",
                "amount": res["details"]["options"]["amount"],
                "unrealised_pnl": res["details"]["options"]["unrealised_pnl"],
            },
            "payment": {
                "currency": "USDT",
                "amount": res["details"]["payment"]["amount"],
            },
            "quant": {"currency": "USDT", "amount": res["details"]["quant"]["amount"]},
            "spot": {"currency": "USDT", "amount": res["details"]["spot"]["amount"]},
        },
        "total": {
            "amount": res["total"]["amount"],
            "borrowed": res["total"]["borrowed"],
            "currency": res["total"]["currency"],
            "unrealised_pnl": res["total"]["unrealised_pnl"],
        },
    }


def get_position_now(url="/futures/usdt/positions"):
    try:
        host = "https://api.gateio.ws"
        prefix = "/api/v4"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        sign_headers = gen_sign("GET", prefix + url, "")
        headers.update(sign_headers)
        response = requests.get(host + prefix + url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        # Filter and return positions with non-zero value
        return [
            (v["contract"], v["value"], v["realised_pnl"], v["unrealised_pnl"])
            for v in data
            if v["value"] != "0"
        ]
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def fetch_btc_price():
    exchange = ccxt.binance()
    current_time = datetime.now()
    past_time = current_time - timedelta(days=1)
    since = int(past_time.timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1h", since=since)
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df


# def plot_candlestick_mplfinance(df):
#     df_plot = df.reset_index()
#     mpf.plot(df_plot.set_index('timestamp'), type='candle', style='charles',
#              title='BTC/USDT Candlestick Chart - Last 24 Hours - mplfinance',
#              ylabel='Price (USDT)',
#              volume=False,
#              show_nontrading=True)


def display_account_info(account_info, max_loops=3, sleep_seconds=10):
    for _ in range(max_loops):
        os.system("clear")  # Clear the terminal before displaying updated information
        console = Console()

        details_table = Table(
            show_header=True, header_style="bold magenta", box=box.DOUBLE_EDGE
        )
        details_table.add_column("Section 📂", style="dim", width=12)
        details_table.add_column("Currency 💵", min_width=10)
        details_table.add_column("Amount 💰", min_width=15)
        details_table.add_column("Unrealised PnL 📉", min_width=20)

        for section, info in account_info["details"].items():
            emoji = "🔵" if float(info["amount"]) > 0 else "🔴"
            pnl_emoji = "🟢" if float(info.get("unrealised_pnl", "0")) >= 0 else "🔴"
            details_table.add_row(
                f"{emoji} {section.capitalize()}",
                info["currency"],
                f"{emoji} {info['amount']}",
                f"{pnl_emoji} {info.get('unrealised_pnl', 'N/A')}",
            )

        console.print(
            Panel(
                details_table,
                title=f"[bold cyan]Account Details",
                subtitle="Sections Overview",
                expand=False,
            )
        )

        print("\n")

        total_info = account_info["total"]
        total_table = Table(
            show_header=True, header_style="bold green", box=box.ROUNDED
        )
        total_table.add_column("Total Amount 💎", style="bold", min_width=15)
        total_table.add_column("Borrowed 🏦", min_width=10)
        total_table.add_column("Currency 💵", min_width=10)
        total_table.add_column("Unrealised PnL 📊", min_width=15)
        total_emoji = "🟢" if float(total_info["amount"]) > 0 else "🔴"
        pnl_emoji = "🟢" if float(total_info["unrealised_pnl"]) >= 0 else "🔴"
        total_table.add_row(
            f"{total_emoji} {total_info['amount']}",
            f"{total_emoji} {total_info['borrowed']}",
            total_info["currency"],
            f"{pnl_emoji} {total_info['unrealised_pnl']}",
        )

        console.print(
            Panel(
                total_table,
                title="[bold blue]Total Account Balance[/]",
                subtitle="Overall Financial Status",
                expand=False,
            )
        )

        print("\n")
        positions = get_position_now()
        if positions:
            total_value = total_realised_pnl = total_unrealised_pnl = 0.0
            positions_table = Table(
                show_header=True, header_style="bold blue", box=box.SQUARE
            )
            positions_table.add_column("Contract📝", style="dim", width=12)
            positions_table.add_column("Value💵", width=20)
            positions_table.add_column("Realised PnL📘", width=20)
            positions_table.add_column("Un PnL📗", width=20)
            for contract, value, realised_pnl, unrealised_pnl in positions:
                value_emoji = "🔵" if float(value) > 0 else "🔴"
                realised_pnl_emoji = "🟢" if float(realised_pnl) >= 0 else "🔴"
                unrealised_pnl_emoji = "🟢" if float(unrealised_pnl) >= 0 else "🔴"
                positions_table.add_row(
                    f"{contract}",
                    f"{value_emoji} {value}",
                    f"{realised_pnl_emoji} {realised_pnl}",
                    f"{unrealised_pnl_emoji} {unrealised_pnl}",
                )
                total_value += float(value)
                total_realised_pnl += float(realised_pnl)
                total_unrealised_pnl += float(unrealised_pnl)
            # Add the totals row with rounding to two decimal places
            positions_table.add_row(
                "Total",
                f"🔷 {round(total_value, 2)}",  # Rounding total value to two decimal places
                f"🔷 {round(total_realised_pnl, 2)}",  # Rounding total realized PnL to two decimal places
                f"🔷 {round(total_unrealised_pnl, 2)}",  # Rounding total unrealized PnL to two decimal places
            )

            console.print(
                Panel(
                    positions_table,
                    title="[bold green]Current Positions[/]",
                    subtitle="Futures Contracts Overview",
                    expand=False,
                )
            )

        time.sleep(sleep_seconds)


def font_examples():
    from colorama import Fore, Back, Style, init

    # 初始化 colorama
    init(autoreset=True)

    # 打印所有前景色
    print(Fore.BLACK + "Black text")
    print(Fore.RED + "Red text")
    print(Fore.GREEN + "Green text")
    print(Fore.YELLOW + "Yellow text")
    print(Fore.BLUE + "Blue text")
    print(Fore.MAGENTA + "Magenta text")
    print(Fore.CYAN + "Cyan text")
    print(Fore.WHITE + "White text")

    # 打印所有背景色
    print(Back.BLACK + "Black background")
    print(Back.RED + "Red background")
    print(Back.GREEN + "Green background")
    print(Back.YELLOW + "Yellow background")
    print(Back.BLUE + "Blue background")
    print(Back.MAGENTA + "Magenta background")
    print(Back.CYAN + "Cyan background")
    print(Back.WHITE + "White background")

    # 打印所有样式
    print(Style.DIM + "Dim text")
    print(Style.NORMAL + "Normal text")
    print(Style.BRIGHT + "Bright text")

    # 组合样式和颜色
    print(Fore.RED + Back.YELLOW + "Red text on yellow background")
    print(Fore.CYAN + Style.BRIGHT + "Bright cyan text")
    print(Fore.GREEN + Style.DIM + "Dim green text")


def get_history_contract(url="/futures/usdt/my_trades"):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    query_param = ""
    sign_headers = gen_sign("GET", prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request("GET", host + prefix + url, headers=headers)
    return r.json()


def get_candlesticks(contract_name: str = "BTC_USDT", n: int = 1, interval: str = "15m"):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = "/futures/usdt/candlesticks"
    query_param = f"contract={contract_name}&limit=20&interval={interval}"
    r = requests.request(
        "GET", host + prefix + url + "?" + query_param, headers=headers
    )
    df = pd.DataFrame(r.json())
    df["Datetime"] = pd.to_datetime(df["t"], unit="s") + timedelta(hours=8)
    df["Symbol"] = contract_name
    df.columns = [
        "Open",
        "Volume",
        "Time",
        "Close",
        "Low",
        "High",
        "Sum",
        "Datetime",
        "Symbol",
    ]
    df = df[["Symbol", "Datetime", "Volume", "Open", "Close", "Low", "High"]]
    df.set_index("Datetime", inplace=True)
    return df.tail(n)


if __name__ == "__main__":
    account_info = fetch_account_info()
    display_account_info(account_info, max_loops=3, sleep_seconds=1)

    print("Data Science Lab Testing here" + "---" * 22)
    print("🤑Your Last 10 History Orders here...")
    # 忽略 SettingWithCopyWarning
    pd.options.mode.chained_assignment = None  # default='warn'


    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = "/futures/usdt/position_close"
    query_param = ""
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign("GET", prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request("GET", host + prefix + url, headers=headers)
    df = pd.DataFrame(r.json())

    columns = [
        "contract",
        "time",
        "side",
        "accum_size",
        "max_size",
        "long_price",
        "short_price",
        "pnl",
        "pnl_pnl",
        "pnl_fee",
        "pnl_fund",
    ]
    df_new = df[columns]
    df_new['💵pnl'] = df_new['pnl']
    df_new["datetime"] = pd.to_datetime(df["time"], unit="s") + timedelta(hours=8)
    new_cols = ['contract', 'datetime', 'side', 'accum_size', 'max_size', 'long_price', 'short_price', '💵pnl', 'pnl_pnl', 'pnl_fee', 'pnl_fund']
    #pnl pnl_pnl pnl_fee pnl_fund should be float and round to 2 decimal places
    df_new['💵pnl'] = df_new['💵pnl'].astype(float).round(3)
    df_new['pnl_pnl'] = df_new['pnl_pnl'].astype(float).round(3)
    df_new['pnl_fee'] = df_new['pnl_fee'].astype(float).round(3)
    df_new['pnl_fund'] = df_new['pnl_fund'].astype(float).round(3)
    # print(df_new.info())
    print(df_new[new_cols].head(n=5))

    input_contract_name = input("Type in your Symbol: ").upper() + "_USDT"

    # history_data = get_history_contract()
    # df = pd.DataFrame(history_data)
    # df['create_time'] = pd.to_datetime(df.create_time, unit='s')
    # print(df.head())

    print("Get candlesticks data...Your symbol is: ", input_contract_name)
    
    interval_val = "15m"
    describe_n = 20
    tmp_df = get_candlesticks(contract_name=input_contract_name, n=describe_n, interval=interval_val)
    print(f"The Data of {input_contract_name} interval is: {interval_val}\nShowing {describe_n} records below: ------------------------------------------------------------")
    print(tmp_df)
    print('----' * 22)

    tmp_df['Open'] = tmp_df['Open'].astype(float)
    tmp_df['Close'] = tmp_df['Close'].astype(float)
    tmp_df['Low'] = tmp_df['Low'].astype(float)
    tmp_df['High'] = tmp_df['High'].astype(float)
    print(f"Statistic Describing price below: ------------------------------------------------------")
    print(tmp_df[['Volume', 'Open', 'Close', 'Low', 'High']].describe())
    print('----' * 22)
    
    for i in range(10):
        tmp_df = get_candlesticks(contract_name=input_contract_name, n=1)
        print(tmp_df)

        init(autoreset=True)
        print(
            Back.CYAN
            + f"{input_contract_name} Current 💰 Price is {tmp_df.Close.values[0]}, and the Current Volume is: {tmp_df.Volume.values[0]}"
        )

        time.sleep(1.5)

    print("Rich Young Lucas, I am so proud of you! " + "---" * 22)
