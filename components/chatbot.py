# components/chatbot.py
# Concept: AI Chatbot with tool calling using Groq
# This is the BRAIN of our dashboard!

import json
from groq import Groq

# ===== IMPORTANT CONCEPT: RAG (Retrieval Augmented Generation) =====
# Instead of the AI guessing answers, we GIVE it real data first!
# RAG = Retrieve relevant data → Augment the prompt → Generate answer
# This makes AI answers ACCURATE instead of hallucinated!

NEPSE_KNOWLEDGE = """
You are a NEPSE (Nepal Stock Exchange) AI analyst assistant.
You help Nepali investors understand the stock market.

Key facts about NEPSE:
- NEPSE is Nepal's only stock exchange, established in 1993
- Trading hours: Sunday to Thursday, 11:00 AM to 3:00 PM NPT
- Major sectors: Banking, Hydropower, Insurance, Manufacturing
- NEPSE index tracks overall market performance
- LTP = Last Traded Price (current price)
- Circuit breaker: stocks can't move more than 10% in one day

Always give advice in simple terms. Remind users this is 
educational only, not financial advice.
"""

def create_client(api_key):
    """Create Groq client"""
    return Groq(api_key=api_key)

def get_stock_context(df, symbol=None):
    """Convert stock dataframe to text context for AI"""
    # Concept: We convert our DATA into TEXT so AI can understand it!
    if symbol:
        row = df[df['symbol'] == symbol.upper()]
        if len(row) > 0:
            r = row.iloc[0]
            return f"{r['symbol']}: Price={r['ltp']} NPR, Change={r['change']} ({r['percentChange']}%), Volume={r['volume']}"
    
    # All stocks summary
    context = "Current NEPSE Stock Prices:\n"
    for _, row in df.iterrows():
        direction = "▲" if row['change'] >= 0 else "▼"
        context += f"- {row['symbol']}: {row['ltp']} NPR {direction} {row['percentChange']}%\n"
    return context

def chat(client, question, stock_df, summary=None, chat_history=[]):
    """Send question to AI with stock context"""
    
    # Build stock context
    stock_context = get_stock_context(stock_df)
    
    # Add market summary context
    summary_context = ""
    if summary:
        summary_context = f"""
MARKET SUMMARY:
- Total Turnover: NPR {summary['totalTurnover']/1e9:.2f} Billion
- Total Transactions: {int(summary['totalTransactions']):,}
- Total Traded Shares: {int(summary['totalTradedShares']):,}
- Total Scrips Traded: {int(summary['totalScripsTraded']):,}
"""
    
    system_prompt = NEPSE_KNOWLEDGE + f"\n\nLIVE MARKET DATA:\n{stock_context}\n{summary_context}"
    
    messages = [{"role": "system", "content": system_prompt}]
    
    for h in chat_history[-4:]:
        messages.append(h)
    
    messages.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=500
    )
    
    return response.choices[0].message.content