import streamlit as st
import plotly.graph_objects as go
from data_fetcher import fetch_financial_data, fetch_chart_data
from ai_analyst import generate_market_report

# Safe PDF Generator Import
try:
    import pdf_generator
    if hasattr(pdf_generator, 'create_pdf_report'):
        create_pdf_report = pdf_generator.create_pdf_report
    elif hasattr(pdf_generator, 'generate_pdf_report'):
        create_pdf_report = pdf_generator.generate_pdf_report
    elif hasattr(pdf_generator, 'generate_pdf'):
        create_pdf_report = pdf_generator.generate_pdf
    else:
        create_pdf_report = None
except Exception:
    create_pdf_report = None

st.set_page_config(page_title="FinAgent AI", page_icon="⚡", layout="wide")

# Custom Dark Theme CSS
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Sidebar
st.sidebar.markdown("### ⚡ Agent Control")
ticker = st.sidebar.text_input("Enter Asset / Stock Ticker", value="NVDA").strip().upper()

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Chart Configuration")
chart_type = st.sidebar.radio("Chart Type", ["Candlestick", "Area Line"])
time_horizon = st.sidebar.select_slider("Time Horizon", options=["5d", "1mo", "3mo", "6mo", "1y", "5y"], value="6mo")

run_analysis = st.sidebar.button("🚀 Run AI Analysis")

st.sidebar.markdown("---")
st.sidebar.markdown("<small>Powered by Multi-Agent Data & LLM Engine</small>", unsafe_allow_html=True)

# Main Dashboard Header
st.markdown("## ⚡ Autonomous AI Financial Agent")
st.markdown("<p style='color: #8b949e;'>Real-time market microstructure, technical indicators, and automated institutional equity research.</p>", unsafe_allow_html=True)

if not ticker:
    st.warning("Please enter a valid stock ticker symbol.")
    st.stop()

# Fetch Data
with st.spinner(f"Ingesting real-time feeds for {ticker}..."):
    data = fetch_financial_data(ticker)

# Error Check Guard
if not data or "error" in data:
    error_msg = data.get("error", "Unknown error") if isinstance(data, dict) else "Could not fetch data"
    st.error(f"⚠️ Error fetching data for **{ticker}**: {error_msg}")
    st.info("Tip: For Indian stocks use `.NS` (e.g., `RELIANCE.NS`, `TCS.NS`), or try US tickers like `NVDA`, `AAPL`, `MSFT`.")
    st.stop()

# Safe Key Extraction
company_name = data.get("company_name", ticker)
current_price = data.get("current_price", 0.0)
pct_change = data.get("pct_change", 0.0)
pe_ratio = data.get("pe_ratio", "N/A")

# Metrics Banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div style='background:#161b22;padding:15px;border-radius:10px;'><span style='color:#8b949e;font-size:0.85rem;'>Asset</span><br><b style='font-size:1.3rem;color:white;'>{company_name[:18]}</b></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='background:#161b22;padding:15px;border-radius:10px;'><span style='color:#8b949e;font-size:0.85rem;'>Live Price</span><br><b style='font-size:1.3rem;color:white;'>${current_price:,.2f}</b></div>", unsafe_allow_html=True)
with col3:
    color = "#238636" if pct_change >= 0 else "#da3633"
    prefix = "+" if pct_change >= 0 else ""
    st.markdown(f"<div style='background:#161b22;padding:15px;border-radius:10px;'><span style='color:#8b949e;font-size:0.85rem;'>24h Change</span><br><b style='font-size:1.3rem;color:{color};'>{prefix}{pct_change:.2f}%</b></div>", unsafe_allow_html=True)
with col4:
    pe_val = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else str(pe_ratio)
    st.markdown(f"<div style='background:#161b22;padding:15px;border-radius:10px;'><span style='color:#8b949e;font-size:0.85rem;'>Trailing P/E</span><br><b style='font-size:1.3rem;color:white;'>{pe_val}</b></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Technical Chart Section
chart_df = fetch_chart_data(ticker, period=time_horizon)

if chart_df is not None and not chart_df.empty:
    fig = go.Figure()
    if chart_type == "Candlestick" and all(col in chart_df.columns for col in ['Open', 'High', 'Low', 'Close']):
        fig.add_trace(go.Candlestick(
            x=chart_df.index,
            open=chart_df['Open'],
            high=chart_df['High'],
            low=chart_df['Low'],
            close=chart_df['Close'],
            name=ticker
        ))
    else:
        close_col = 'Close' if 'Close' in chart_df.columns else chart_df.columns[0]
        fig.add_trace(go.Scatter(
            x=chart_df.index,
            y=chart_df[close_col],
            mode='lines',
            line=dict(color='#3b82f6', width=2),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)',
            name=ticker
        ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_rangeslider_visible=False,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Technical chart data currently unavailable for this horizon.")

# AI Research Memo Section
if run_analysis:
    st.markdown("---")
    st.markdown("### 🧠 Autonomous Equity Research Memo")
    
    with st.spinner("Synthesizing quantitative indicators & news with Groq LLM..."):
        report_text = generate_market_report(data)
        st.markdown(report_text)
        
        if create_pdf_report:
            try:
                pdf_bytes = create_pdf_report(data, report_text)
                if pdf_bytes:
                    st.download_button(
                        label="📥 Download Institutional Research Note (PDF)",
                        data=pdf_bytes,
                        file_name=f"{ticker}_Research_Report.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.warning("PDF generation temporarily unavailable.")
