import yfinance as yf
import ta
import requests
import time

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
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
    data = yf.download("TSLA", period="3mo", interval="1d")

    close_prices = data["Close"].squeeze()

    data["EMA20"] = ta.trend.EMAIndicator(close_prices, window=20).ema_indicator()
    data["EMA50"] = ta.trend.EMAIndicator(close_prices, window=50).ema_indicator()
    data["RSI"] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()

    latest = data.iloc[-1]

    close = float(latest["Close"])
    ema20 = float(latest["EMA20"])
    ema50 = float(latest["EMA50"])
    rsi = float(latest["RSI"])

    print("\nTSLA Price:", round(close, 2))
    print("EMA20:", round(ema20, 2))
    print("EMA50:", round(ema50, 2))
    print("RSI:", round(rsi, 2))

    if close > ema20 and ema20 > ema50 and rsi > 50 and rsi < 70:
        print("BUY SIGNAL")
        send_telegram_message("🚀 BUY SIGNAL for TSLA")

    elif close < ema20 or rsi > 75 or rsi < 45:
        print("SELL SIGNAL")
        send_telegram_message("🔴 SELL SIGNAL for TSLA")

    else:
        print("NO CLEAR SIGNAL")
        send_telegram_message("No clear signal for TSLA")

    time.sleep(3600)
