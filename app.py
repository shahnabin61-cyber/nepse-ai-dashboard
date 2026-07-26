# app.py
# Main Streamlit Dashboard
# Run with: streamlit run app.py

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.nepse_data import get_top_stocks, get_market_summary
from components.charts import plot_stock_prices, plot_gainers_losers, plot_volume
from components.chatbot import create_client, chat

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="NEPSE AI Dashboard",
    page_icon="📈",
    layout="wide"
)

# ===== HEADER =====
st.title("📈 NEPSE AI Stock Dashboard")
st.caption("Nepal Stock Exchange — Live Market Analysis + AI Chatbot")
st.divider()

# ===== SIDEBAR =====
st.sidebar.title("⚙️ Settings")
import os
api_key = st.secrets.get("GROQ_API_KEY", None) or st.sidebar.text_input("Groq API Key", type="password")
st.sidebar.divider()
st.sidebar.markdown("**About**")
st.sidebar.info("Built with Python, Streamlit, Plotly & Groq AI")

# ===== LOAD DATA =====
with st.spinner("Loading market data..."):
    df = get_top_stocks()
    summary = get_market_summary()

# ===== KPI METRICS =====
st.subheader("📊 Market Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Market Cap (NPR)",
        value=f"{summary['nepseIndex']:,.2f}B",
    )
with col2:
    st.metric(
        label="Total Turnover",
        value=f"NPR {summary['totalTurnover']/1e9:.2f}B"
    )
with col3:
    st.metric(
        label="Transactions",
        value=f"{int(summary['totalTransactions']):,}"
    )
with col4:
    st.metric(
        label="Scrips Traded",
        value=f"{int(summary['totalScripsTraded']):,}"
    )
st.divider()

# ===== CHARTS =====
st.subheader("📉 Stock Analysis")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(plot_stock_prices(df), use_container_width=True)

with col2:
    st.plotly_chart(plot_gainers_losers(df), use_container_width=True)

st.plotly_chart(plot_volume(df), use_container_width=True)

st.divider()

# ===== AI CHATBOT =====
st.subheader("🤖 Ask AI Analyst")

if not api_key:
    st.warning("⚠️ Please enter your Groq API key in the sidebar to use the AI chatbot!")
else:
    client = create_client(api_key)

    # Chat history stored in session
    # Concept: st.session_state keeps data alive between interactions!
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    question = st.chat_input("Ask about NEPSE stocks... e.g. Which stock is performing best today?")

    if question:
        # Show user message
        with st.chat_message("user"):
            st.write(question)

        # Get AI answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chat(client, question, df, summary, st.session_state.chat_history)
            st.write(answer)

        # Save to history
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})