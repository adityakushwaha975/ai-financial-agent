import os
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from ai_analyst import generate_market_report
from data_fetcher import fetch_financial_data
from pdf_generator import create_financial_pdf

# Page Setup
st.set_page_config(
    page_title="FinAgent AI | Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# External CSS File Loader Function
def load_css(file_name: str):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load External Styles
load_css("style.css")

# Sidebar Controls
with st.sidebar:
    st.markdown("### ⚡ **Agent Control**")
    ticker = st.text_input("Enter Asset / Stock Ticker", value="RELIANCE.NS").upper().strip()
    
    st.markdown("---")
    st.markdown("##### ⚙️ Chart Configuration")
    chart_type = st.radio("Chart Type", ["Candlestick", "Area Line"], horizontal=True)
    time_period = st.select_slider(
        "Time Horizon",
        options=["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        value="6mo"
    )
    
    st.markdown("---")
    analyze_btn = st.button("🚀 Run AI Analysis", type="primary")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Powered by Multi-Agent Data & LLM Engine")

# Header Section
st.markdown('<div class="hero-title">⚡ Autonomous AI Financial Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Real-time market microstructure, technical indicators, and automated institutional equity research.</div>', unsafe_allow_html=True)

if ticker:
    with st.spinner("Fetching live market data..."):
        data = fetch_financial_data(ticker)
    
    if "error" in data:
        st.error(f"❌ Error fetching data for {ticker}: {data['error']}")
    else:
        # 1. Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        
        change_val = data.get('1d_change_percent', 0.0)
        is_pos = change_val >= 0
        delta_class = "metric-delta-pos" if is_pos else "metric-delta-neg"
        arrow = "▲" if is_pos else "▼"
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Asset / Company</div>
                <div class="metric-value" style="font-size: 1.3rem;">{data['company_name'][:18]}</div>
                <span style="color: #38BDF8; font-weight:600; font-size: 0.85rem;">{data['symbol']}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Live Price</div>
                <div class="metric-value">{data['currency']} {data['current_price']}</div>
                <span class="{delta_class}">{arrow} {change_val}% Today</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Valuation (P/E)</div>
                <div class="metric-value">{data['pe_ratio']}</div>
                <span style="color: #94A3B8; font-size: 0.85rem;">Trailing Multiple</span>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Market Status</div>
                <div class="metric-value" style="font-size: 1.3rem; color: #34D399;">● ACTIVE</div>
                <span style="color: #94A3B8; font-size: 0.85rem;">Realtime Stream</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Interactive Plotly Charts
        st.markdown(f"#### 📊 **{data['company_name']} ({ticker}) Price Action**")
        stock = yf.Ticker(ticker)
        hist = stock.history(period=time_period)

        if not hist.empty:
            fig = go.Figure()

            if chart_type == "Candlestick" and len(hist) > 1:
                fig.add_trace(go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name='Price Action',
                    increasing_line_color='#10B981',
                    decreasing_line_color='#EF4444'
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=hist['Close'],
                    fill='tozeroy',
                    fillcolor='rgba(56, 189, 248, 0.1)',
                    line=dict(color='#38BDF8', width=2.5),
                    name='Close Price'
                ))

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.4)",
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', rangeslider=dict(visible=False)),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', side="right"),
                margin=dict(l=20, r=20, t=20, b=20),
                height=420,
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)

        # 3. AI Equity Research Section
        st.markdown("---")
        st.markdown("### 🧠 **Autonomous Equity Research Report**")
        
        # State management taaki page refresh par analysis gayab na ho
        if "report_cache" not in st.session_state:
            st.session_state.report_cache = {}

        if analyze_btn:
            with st.spinner("🤖 Multi-agent synthesis: reading news & calculating verdict..."):
                report = generate_market_report(ticker)
                st.session_state.report_cache[ticker] = report

        current_report = st.session_state.report_cache.get(ticker)

        if current_report:
            # Report card container
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown(current_report)
            st.markdown('</div>', unsafe_allow_html=True)

            # Generate PDF in background
            pdf_bytes = create_financial_pdf(data, current_report)

            st.markdown("<br>", unsafe_allow_html=True)
            col_pdf, _ = st.columns([1, 3])
            with col_pdf:
                st.download_button(
                    label="📥 Download Research Note (PDF)",
                    data=pdf_bytes,
                    file_name=f"{ticker}_Equity_Research_Note.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("💡 Click **'🚀 Run AI Analysis'** in the sidebar to generate comprehensive institutional research.")