import yfinance as yf
import ta
import requests
import time

TOKEN = "8392925173:AAHF0DUwzoL1fXGDPJwXLmvASJSuVOZk1X4"
CHAT_ID = "1702453586"

STOCKS = ["TSLA", "NVDA", "AAPL"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    print(response.text)


def analyze_stock(ticker):
    data = yf.download(ticker, period="1y", interval="1d")
    close_prices = data["Close"].squeeze()

    data["EMA20"] = ta.trend.EMAIndicator(close_prices, window=20).ema_indicator()
    data["EMA50"] = ta.trend.EMAIndicator(close_prices, window=50).ema_indicator()
    data["EMA100"] = ta.trend.EMAIndicator(close_prices, window=100).ema_indicator()
    data["RSI"] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()
    data["VolumeAVG20"] = data["Volume"].rolling(window=20).mean()

    latest = data.iloc[-1]

    close = float(latest["Close"])
    ema20 = float(latest["EMA20"])
    ema50 = float(latest["EMA50"])
    ema100 = float(latest["EMA100"])
    rsi = float(latest["RSI"])
    volume = float(latest["Volume"])
    volume_avg = float(latest["VolumeAVG20"])

    support = float(data["Low"].tail(30).min())
    resistance = float(data["High"].tail(30).max())

    if close > ema20 > ema50 > ema100:
        trend = "Bullish 📈"
    elif close < ema20 < ema50 < ema100:
        trend = "Bearish 📉"
    else:
        trend = "Neutral ⚪"

    if volume > volume_avg * 1.5:
        volume_status = "High 🔥"
    elif volume < volume_avg * 0.7:
        volume_status = "Low 💤"
    else:
        volume_status = "Normal"

    if close > ema20 and ema20 > ema50 and ema50 > ema100 and rsi > 50 and rsi < 70:
        signal = "BUY 🚀"
    elif close < ema20 or rsi > 75 or rsi < 45:
        signal = "SELL 🔴"
    else:
        signal = "WAIT ⚪"

    message = f"""
📊 {ticker} Stock Analysis

Price: {round(close, 2)}

Trend: {trend}
Volume: {volume_status}

EMA20: {round(ema20, 2)}
EMA50: {round(ema50, 2)}
EMA100: {round(ema100, 2)}

RSI: {round(rsi, 2)}

Support: {round(support, 2)}
Resistance: {round(resistance, 2)}

Signal: {signal}
"""

    print(message)
    send_telegram_message(message)


while True:
    for stock in STOCKS:
        analyze_stock(stock)

    time.sleep(3600)