import requests

API_URL = "https://api.gateio.ws/api/v4/futures/usdt/contracts"

def get_future_price(symbol):
    """
    Fetches the future price of a given cryptocurrency symbol from Gate.io API v4.
    
    Args:
        symbol (str): The symbol of the cryptocurrency futures contract, e.g., "BTC_USDT".
    
    Returns:
        float: The future price of the cryptocurrency, or None if an error occurs.
    """
    try:
        # The endpoint for the specific cryptocurrency futures contract's ticker
        request_url = f"{API_URL}/{symbol}/ticker"
        # Send the GET request to the Gate.io API
        response = requests.get(request_url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
        # Parse the JSON response
        data = response.json()
        # Return the mark price (or last price)
        return float(data['mark_price'])
    except Exception as e:
        print(f"An error occurred while fetching the future price for {symbol}: {e}")
        return None
