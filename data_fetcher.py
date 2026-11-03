import yfinance as yf
import pandas as pd
import requests

# Custom session taaki Cloud IP bot-block bypass ho sake
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

def fetch_financial_data(ticker_symbol: str) -> dict:
    try:
        ticker_symbol = ticker_symbol.strip().upper()
        stock = yf.Ticker(ticker_symbol, session=session)
        
        # History fetch with fallback
        try:
            history = stock.history(period="5d")
        except Exception:
            stock = yf.Ticker(ticker_symbol)
            history = stock.history(period="5d")

        if history.empty:
            return {"error": f"Invalid ticker: {ticker_symbol}"}

        current_price = history['Close'].iloc[-1]
        prev_close = history['Close'].iloc[-2] if len(history) > 1 else current_price
        pct_change = ((current_price - prev_close) / prev_close) * 100

        try:
            info = stock.info or {}
        except Exception:
            info = {}

        try:
            raw_news = stock.news or []
        except Exception:
            raw_news = []

        formatted_news = []
        for item in raw_news[:4]:
            title = item.get('title')
            if not title and 'content' in item:
                title = item['content'].get('title')
            if title:
                formatted_news.append(title)

        return {
            "symbol": ticker_symbol,
            "current_price": float(current_price),
            "pct_change": float(pct_change),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "news": formatted_news,
            "history": history
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_chart_data(ticker_symbol: str, period: str = "6mo"):
    try:
        ticker_symbol = ticker_symbol.strip().upper()
        # Direct download Cloud deployment par zyada stable rehta hai
        df = yf.download(ticker_symbol, period=period, progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if df.empty:
            stock = yf.Ticker(ticker_symbol, session=session)
            df = stock.history(period=period)
        return df
    except Exception:
        stock = yf.Ticker(ticker_symbol)
        return stock.history(period=period)
