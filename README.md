# ⚡ FinAgent AI: Autonomous Financial & Equity Research Terminal

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LLM Engine](https://img.shields.io/badge/Groq-Fast%20Inference-f55036.svg?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

An institutional-grade, full-stack Autonomous AI Financial Research Terminal that fetches real-time market microstructure, technical price action, and corporate news, synthesizing them using High-Performance LLMs via Groq to produce comprehensive equity research notes and downloadable PDF reports.

---

## 📌 Table of Contents
1. Project Overview
2. Key Capabilities
3. Supported Asset Tickers
4. System Architecture
5. Tech Stack
6. Repository Structure
7. Local Setup & Installation
8. Environment Configuration
9. Deployment (Streamlit Cloud)
10. License

---

## 🚀 Project Overview

Retail traders and analysts routinely spend hours aggregating fragmented market data across news portals, valuation charts, and SEC filings. 

FinAgent AI standardizes this end-to-end workflow:
- Ingests Real-Time Feeds: Live pricing, daily variations, market multiples (Trailing P/E), and corporate news headlines.
- Interactive Visualization: Multi-timeframe Plotly candlestick and area line charts (5d to 5y).
- Autonomous Multi-Agent Synthesis: Analyzes company fundamentals against prevailing macroeconomic sentiment.
- Structured Report Generation: Delivers a 4-part research memo (Valuation, Sentiment, Bull/Bear Cases, Final Stance).
- Institutional PDF Export: One-click automated PDF research note compiled via ReportLab.

---

## ✨ Key Capabilities

- 📈 Real-Time Data Ingestion: Live streaming market data and historical price points powered by Yahoo Finance (`yfinance`).
- 🧠 Ultra-Fast LLM Inference: Powered by Groq Cloud for instant multi-perspective financial synthesis.
- 📊 Interactive Technical Charting: Dynamic candlesticks with volume indicators and custom moving horizons.
- 📑 Instant PDF Export: Generates standardized, single-page print-ready institutional research memos.
- 🎨 Bloomberg-Grade UI: Dark-terminal theme with glassmorphic cards and responsive layouts.

---

## 🔍 Supported Asset Tickers

The terminal accepts valid ticker symbols supported by Yahoo Finance. Below are standard tickers ready for search:

### 🇮🇳 Indian Equities (NSE)
Note: Suffix `.NS` is required for Indian National Stock Exchange listings.
- `RELIANCE.NS` – Reliance Industries
- `TCS.NS` – Tata Consultancy Services
- `INFY.NS` – Infosys
- `HDFCBANK.NS` – HDFC Bank
- `TATAMOTORS.NS` – Tata Motors
- `ITC.NS` – ITC Limited
- `SBIN.NS` – State Bank of India

### 🇺🇸 US & Global Tech Stocks
- `NVDA` – NVIDIA Corporation
- `AAPL` – Apple Inc.
- `MSFT` – Microsoft Corporation
- `TSLA` – Tesla Inc.
- `GOOGL` – Alphabet Inc.
- `AMZN` – Amazon.com Inc.
- `META` – Meta Platforms

### 🌐 Digital Assets & Crypto
- `BTC-USD` – Bitcoin
- `ETH-USD` – Ethereum
- `SOL-USD` – Solana

### 📊 Market Indices & Commodities
- `^NSEI` – Nifty 50 Index
- `^BSESN` – BSE Sensex Index
- `GC=F` – Gold Futures
- `CL=F` – Crude Oil Futures

---

## 🏗️ System Architecture


       ┌─────────────────────────────────────────────────────────┐
       │                 User Web Interface                      │
       │           (Streamlit + Custom Modular CSS)              │
       └────────────────────────────┬────────────────────────────┘
                                    │
                    ┌───────────────┴──────────────┐
                    ▼                              ▼
      ┌───────────────────────────┐  ┌───────────────────────────┐
      │   Market Data Ingestion   │  │   Interactive Plotly UI   │
      │   (data_fetcher.py)       │  │ (Candlestick / Area Chart)│
      │   - Live Prices & P/E     │  └───────────────────────────┘
      │   - Real-time News Feeds  │
      └─────────────┬─────────────┘
                    │
                    ▼
      ┌───────────────────────────┐
      │     LLM Research Agent    │
      │     (ai_analyst.py)       │
      │     - Multi-Agent Logic   │
      │     - Groq Cloud Engine   │
      └─────────────┬─────────────┘
                    │
                    ▼
      ┌───────────────────────────┐
      │   Institutional Export    │
      │   (pdf_generator.py)      │
      │   - ReportLab PDF Engine  │
      └───────────────────────────┘
