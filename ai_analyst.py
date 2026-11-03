import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_market_report(data_input) -> str:
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "⚠️ Groq API Key missing. Please set GROQ_API_KEY in Streamlit Secrets."

        client = Groq(api_key=api_key)

        # Handle both dict and string inputs safely
        if isinstance(data_input, dict):
            symbol = str(data_input.get("symbol", "ASSET")).strip()
            name = str(data_input.get("company_name", symbol)).strip()
            price = data_input.get("current_price", "N/A")
            change = data_input.get("pct_change", "N/A")
            pe = data_input.get("pe_ratio", "N/A")
            news_items = data_input.get("news", [])
            news_text = "\n".join([f"- {n}" for n in news_items]) if news_items else "No major news headlines."
        else:
            symbol = str(data_input).strip()
            name = symbol
            price = "N/A"
            change = "N/A"
            pe = "N/A"
            news_text = "Market tracking data."

        prompt = f"""
You are a senior institutional equity research analyst. Analyze the following asset and write a structured investment memo:

Company/Asset: {name} ({symbol})
Current Price: ${price}
24h Performance: {change}%
Trailing P/E: {pe}

Recent News Highlights:
{news_text}

Provide your synthesis strictly divided into these 4 sections:
1. Executive Valuation & Multiples Overview
2. Macro & Sentiment Dynamics
3. Bull Case vs Bear Case
4. Strategic Verdict & Conviction Score (1-10)
"""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional financial equity analyst delivering sharp institutional research notes."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
