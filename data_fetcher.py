import yfinance as yf
import pprint

def fetch_financial_data(ticker_symbol: str) -> dict:
    try:
        stock = yf.Ticker(ticker_symbol)
        history = stock.history(period="5d")
        
        if history.empty:
            return {"error": f"Invalid ticker: {ticker_symbol}"}
            
        current_price = history['Close'].iloc[-1]
        prev_close = history['Close'].iloc[-2] if len(history) > 1 else current_price
        pct_change = ((current_price - prev_close) / prev_close) * 100

        info = stock.info or {}
        raw_news = stock.news or []
        
        formatted_news = []
        for item in raw_news[:4]:
            # Yahoo finance newer vs older structure handling
            title = item.get('title')
            publisher = item.get('publisher', 'Financial Media')
            
            if not title and 'content' in item:
                content = item.get('content', {})
                title = content.get('title')
                provider = content.get('provider', {})
                publisher = provider.get('displayName', 'Financial Media')
            
            if title:
                formatted_news.append({
                    "headline": title,
                    "publisher": publisher
                })

        return {
            "symbol": ticker_symbol.upper(),
            "company_name": info.get("longName", ticker_symbol.upper()),
            "current_price": round(float(current_price), 2),
            "currency": info.get("currency", "INR"),
            "1d_change_percent": round(float(pct_change), 2),
            "pe_ratio": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
            "news": formatted_news
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Testing Reliance Data Fetch with Updated News Parser:")
    pprint.pprint(fetch_financial_data("RELIANCE.NS"))