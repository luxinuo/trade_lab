import requests
from lib.lucas_gate import get_future_price
from tabulate import tabulate

def main():
    # Define the cryptocurrencies and the corresponding future market symbols
    cryptos = {
        'BTC': 'BTC_USDT',
        'ETH': 'ETH_USDT',
    }

    prices = []

    for crypto, symbol in cryptos.items():
        # Fetch the future price
        price = get_future_price(symbol)
        if price:
            prices.append([crypto, price])
        else:
            prices.append([crypto, 'Error fetching price'])

    # Format and print the output
    print(tabulate(prices, headers=['Crypto', 'Future Price (USDT)'], tablefmt='pretty'))

if __name__ == '__main__':
    main()