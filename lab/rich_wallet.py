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




def gen_sign(method, url, query_string=None, payload_string=None):
    sign_path = "../cred/credentials.json"

    # Read the credentials from the file
    with open(sign_path, 'r') as f:
        data = json.load(f)
        key = data['pub_key']
        secret = data['secret_key']

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

def get_data():
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    # url = '/account/detail'
    url = '/wallet/total_balance'
    query_param = ''
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    # print(r.json())
    return r.json()

def fetch_account_info_test():
    res = get_data()
    return {
        "details": {
            "delivery": {"currency": "USDT", "amount": res["details"]["delivery"]["amount"], "unrealised_pnl": res["details"]["delivery"]["unrealised_pnl"]},
            "finance": {"currency": "USDT", "amount": res["details"]["finance"]["amount"]},
            "futures": {"currency": "USDT", "amount": res["details"]["futures"]["amount"], "unrealised_pnl": res["details"]["futures"]["unrealised_pnl"]},
            "margin": {"currency": "USDT", "amount": res["details"]["margin"]["amount"], "borrowed": res["details"]["margin"]["borrowed"]},
            "options": {"currency": "USDT", "amount": res["details"]["options"]["amount"], "unrealised_pnl": res["details"]["options"]["unrealised_pnl"]},
            "payment": {"currency": "USDT", "amount": res["details"]["payment"]["amount"]},
            "quant": {"currency": "USDT", "amount": res["details"]["quant"]["amount"]},
            "spot": {"currency": "USDT", "amount": res["details"]["spot"]["amount"]}
        },
        "total": {
            "amount": res["total"]["amount"],
            "borrowed": res["total"]["borrowed"],
            "currency": res["total"]["currency"],
            "unrealised_pnl": res["total"]["unrealised_pnl"]
        }
    }

# Mock-up function for fetching data - replace this with your actual fetching logic
def fetch_account_info():
    res = get_data()
    return {
        "details": {
            "delivery": {"currency": "USDT", "amount": res["details"]["delivery"]["amount"], "unrealised_pnl": res["details"]["delivery"]["unrealised_pnl"]},
            "finance": {"currency": "USDT", "amount": res["details"]["finance"]["amount"]},
            "futures": {"currency": "USDT", "amount": res["details"]["futures"]["amount"], "unrealised_pnl": res["details"]["futures"]["unrealised_pnl"]},
            "margin": {"currency": "USDT", "amount": res["details"]["margin"]["amount"], "borrowed": res["details"]["margin"]["borrowed"]},
            "options": {"currency": "USDT", "amount": res["details"]["options"]["amount"], "unrealised_pnl": res["details"]["options"]["unrealised_pnl"]},
            "payment": {"currency": "USDT", "amount": res["details"]["payment"]["amount"]},
            "quant": {"currency": "USDT", "amount": res["details"]["quant"]["amount"]},
            "spot": {"currency": "USDT", "amount": res["details"]["spot"]["amount"]}
        },
        "total": {
            "amount": res["total"]["amount"],
            "borrowed": res["total"]["borrowed"],
            "currency": res["total"]["currency"],
            "unrealised_pnl": res["total"]["unrealised_pnl"]
        }
    }

def display_account_info(account_info):
    console = Console()
    
    # Add a column for input your name:
    # name = input("Enter your name: ")
    # console.print(f"Hello, {name}! Here's your account information:")

    details_table = Table(show_header=True, header_style="bold magenta", box=box.DOUBLE_EDGE)
    details_table.add_column("Section 📂", style="dim", width=12)
    details_table.add_column("Currency 💵", min_width=10)
    details_table.add_column("Amount 💰", min_width=15)
    details_table.add_column("Unrealised PnL 📉", min_width=20)

    for section, info in account_info['details'].items():
        emoji = "🔵" if float(info['amount']) > 0 else "🔴"
        pnl_emoji = "🟢" if float(info.get('unrealised_pnl', '0')) >= 0 else "🔴"
        details_table.add_row(
            f"{emoji} {section.capitalize()}",
            info['currency'],
            f"{emoji} {info['amount']}",
            f"{pnl_emoji} {info.get('unrealised_pnl', 'N/A')}"  # Not all sections have unrealised_pnl
        )

    console.print(Panel(details_table, title=f"[bold cyan]Account Details: Lucas Lee[/]", subtitle="Sections Overview", expand=False))

    total_info = account_info['total']
    total_table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
    total_table.add_column("Total Amount 💎", style="bold", min_width=15)
    total_table.add_column("Borrowed 🏦", min_width=10)
    total_table.add_column("Currency 💵", min_width=10)
    total_table.add_column("Unrealised PnL 📊", min_width=15)
    total_emoji = "🟢" if float(total_info['amount']) > 0 else "🔴"
    pnl_emoji = "🟢" if float(total_info['unrealised_pnl']) >= 0 else "🔴"
    total_table.add_row(
        f"{total_emoji} {total_info['amount']}",
        f"{total_emoji} {total_info['borrowed']}",
        total_info['currency'],
        f"{pnl_emoji} {total_info['unrealised_pnl']}"
    )

    console.print(Panel(total_table, title="[bold blue]Total Account Balance[/]", subtitle="Overall Financial Status", expand=False))

if __name__ == "__main__":
    account_info = fetch_account_info()
    display_account_info(account_info)
    # print(json.dumps(account_info))
