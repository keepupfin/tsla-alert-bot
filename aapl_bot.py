import yfinance as yf
import ta
import requests
import time

TOKEN = "8392925173:AAHF0DUwzoL1fXGDPJwXLmvASJSuVOZk1X4"
CHAT_ID = "1702453586"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    print(response.text)


while True:
    data = yf.download("AAPL", period="1y", interval="1d")

    close_prices = data["Close"].squeeze()

    data["EMA20"] = ta.trend.EMAIndicator(close_prices, window=20).ema_indicator()
    data["EMA50"] = ta.trend.EMAIndicator(close_prices, window=50).ema_indicator()
    data["EMA100"] = ta.trend.EMAIndicator(close_prices, window=100).ema_indicator()
    data["RSI"] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()

    latest = data.iloc[-1]

    close = float(latest["Close"])
    ema20 = float(latest["EMA20"])
    ema50 = float(latest["EMA50"])
    ema100 = float(latest["EMA100"])
    rsi = float(latest["RSI"])

    print("\nAAPL Price:", round(close, 2))
    print("EMA20:", round(ema20, 2))
    print("EMA50:", round(ema50, 2))
    print("EMA100:", round(ema100, 2))
    print("RSI:", round(rsi, 2))

    if close > ema20 and ema20 > ema50 and ema50 > ema100 and rsi > 50 and rsi < 70:
        print("BUY SIGNAL")
        send_telegram_message("🚀 BUY SIGNAL for AAPL")

    elif close < ema20 or rsi > 75 or rsi < 45:
        print("SELL SIGNAL")
        send_telegram_message("🔴 SELL SIGNAL for AAPL")

    else:
        print("NO CLEAR SIGNAL")
        send_telegram_message("No clear signal for AAPL")

    time.sleep(3600)