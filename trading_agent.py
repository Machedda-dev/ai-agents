import yfinance as yf
import ccxt
import json
from ai_agent import query_ollama

def get_stock_price(symbol):
    """Get current stock price using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
    except Exception as e:
        return f"Error: {e}"

def get_crypto_price(symbol):
    """Get current crypto price using ccxt"""
    try:
        exchange = ccxt.binance()
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        return f"Error: {e}"

def analyse_sentiment(asset, price):
    """Analyse sentiment using AI"""
    prompt = f"""
    Based on the current price of {asset} at ${price}, provide a brief sentiment analysis.
    Include:
    1. Current trend (bullish/bearish/neutral)
    2. Key factors affecting the price
    3. Short-term outlook (1-2 weeks)
    """
    return query_ollama(prompt)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python trading_agent.py <symbol>")
        print("  Stock: AAPL, TSLA, GOOGL")
        print("  Crypto: BTC/USDT, ETH/USDT")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    print(f"=== TRADING AGENT: {symbol} ===")

    if "/" in symbol:
        # Crypto
        price = get_crypto_price(symbol)
        if price:
            print(f"Price: ${price:.2f}")
            analysis = analyse_sentiment(symbol, price)
            print(f"\nAI Analysis:\n{analysis}")
        else:
            print("Could not fetch price for", symbol)
    else:
        # Stock
        price = get_stock_price(symbol)
        if price:
            print(f"Price: ${price:.2f}")
            analysis = analyse_sentiment(symbol, price)
            print(f"\nAI Analysis:\n{analysis}")
        else:
            print("Could not fetch price for", symbol)