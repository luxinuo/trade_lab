# main.py

import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Mock-up function for fetching data - replace this with your actual fetching logic
def fetch_account_info():
    # Simulating fetching data from gate.io
    return {
        "details": {
            "delivery": {"currency": "USDT", "amount": "0", "unrealised_pnl": "0"},
            "finance": {"currency": "USDT", "amount": "528.468025"},
            "futures": {"currency": "USDT", "amount": "891.79848731", "unrealised_pnl": "-120.563000000044"},
            "margin": {"currency": "USDT", "amount": "0", "borrowed": "0"},
            "options": {"currency": "USDT", "amount": "0", "unrealised_pnl": "0"},
            "payment": {"currency": "USDT", "amount": "0"},
            "quant": {"currency": "USDT", "amount": "0"},
            "spot": {"currency": "USDT", "amount": "61.35376662"}
        },
        "total": {
            "amount": "1481.62027893",
            "borrowed": "0",
            "currency": "USDT",
            "unrealised_pnl": "-120.563000000044"
        }
    }

def display_account_info(account_info):
    console = Console()

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

    console.print(Panel(details_table, title="[bold cyan]Account Details[/]", subtitle="Sections Overview", expand=False))

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
    account_info = fetch_account_info()  # Replace this with actual API call
    display_account_info(account_info)
