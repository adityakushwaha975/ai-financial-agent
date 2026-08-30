import os
from dotenv import load_dotenv
from groq import Groq
from data_fetcher import fetch_financial_data

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY .env file mein nahi mili!")

client = Groq(api_key=api_key)

def generate_market_report(ticker_symbol: str) -> str:
    print(f"1. Live data fetch ho raha hai: {ticker_symbol}...")
    data = fetch_financial_data(ticker_symbol)
    
    if "error" in data:
        return f"Error: {data['error']}"

    news_text = "\n".join([f"- {n['headline']} (Source: {n['publisher']})" for n in data.get('news', [])])
    if not news_text:
        news_text = "No recent headlines available."

    prompt = f"""
    You are an expert financial market research analyst.
    Analyze the following market data and news:

    Company: {data['company_name']} ({data['symbol']})
    Current Price: {data['current_price']} {data['currency']} (1-Day Change: {data['1d_change_percent']}%)
    P/E Ratio: {data['pe_ratio']}
    
    Recent News:
    {news_text}

    Generate a structured, professional Financial Research Report:
    1. Key Metrics & Valuation Analysis
    2. News & Sentiment Breakdown
    3. Bull Case vs Bear Case (2 bullet points each)
    4. Final Verdict (Bullish / Bearish / Neutral stance with reasoning)

    Keep formatting clean with markdown bullet points.
    """

    print("2. Generating AI report...")
    
    # Pehle exact working model try karega, phir baki active text models
    active_models = ["groq/compound"]
    try:
        fetched = [m.id for m in client.models.list().data if not any(x in m.id for x in ['whisper', 'orpheus', 'tts', 'audio', 'canopylabs'])]
        active_models.extend(fetched)
    except Exception:
        pass

    last_error = ""
    for model_name in active_models:
        try:
            print(f"Using model: {model_name}...")
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            last_error = str(e)
            continue
            
    return f"Error: {last_error}"

if __name__ == "__main__":
    report = generate_market_report("RELIANCE.NS")
    print("\n" + "="*50)
    print(report)
    print("="*50)