# data/nepse_data.py
import pandas as pd
import requests
from datetime import datetime

def get_market_summary():
    """Get overall NEPSE market summary"""
    try:
        from nepse_scraper import NepseScraper
        scraper = NepseScraper(verify_ssl=False)
        raw = scraper.get_market_summary()
        
        # Convert list of detail/value to a clean dict
        summary = {}
        for item in raw:
            summary[item['detail']] = item['value']
        
        # Map to our standard keys
        return {
            'nepseIndex': summary.get('Total Market Capitalization Rs:', 0) / 1e9,
            'change': 0.0,
            'percentageChange': 0.0,
            'totalTurnover': summary.get('Total Turnover Rs:', 0),
            'totalTransactions': summary.get('Total Transactions', 0),
            'totalTradedShares': summary.get('Total Traded Shares', 0),
            'totalScripsTraded': summary.get('Total Scrips Traded', 0)
        }
    except Exception as e:
        print(f"Live data failed: {e}")
        return get_sample_summary()

def get_top_stocks():
    """Get today's top stocks"""
    try:
        from nepse_scraper import NepseScraper
        scraper = NepseScraper(verify_ssl=False)
        prices = scraper.get_today_price()
        df = pd.DataFrame(prices)
        
        # Rename to our standard column names
        df['ltp'] = df['lastUpdatedPrice']
        df['change'] = df['lastUpdatedPrice'] - df['previousDayClosePrice']
        df['percentChange'] = (df['change'] / df['previousDayClosePrice']) * 100
        df['volume'] = df['totalTradedQuantity']
        
        # Keep only needed columns
        df = df[['symbol', 'securityName', 'ltp', 'openPrice', 
                 'highPrice', 'lowPrice', 'change', 'percentChange', 
                 'volume', 'totalTrades']].dropna()
        
        return df
        
    except Exception as e:
        print(f"Live data failed: {e}")
        return get_sample_stocks()

def get_sample_summary():
    """Fallback sample data if NEPSE API is down"""
    return {
        'nepseIndex': 2145.32,
        'change': 12.45,
        'percentageChange': 0.58,
        'totalTurnover': 1234567890,
        'totalTransactions': 45231,
        'totalTradedShares': 3456789
    }

def get_sample_stocks():
    """Fallback sample stock data"""
    data = {
        'symbol': ['NABIL', 'NTC', 'NICA', 'SCB', 'SHIVM', 'ADBL', 'NBB', 'GBIME'],
        'ltp':    [1245.0, 890.0, 456.0, 1890.0, 234.0, 567.0, 345.0, 678.0],
        'change': [15.0, -5.0, 8.0, 25.0, -3.0, 12.0, -8.0, 18.0],
        'percentChange': [1.22, -0.56, 1.79, 1.34, -1.27, 2.16, -2.27, 2.73],
        'volume': [12345, 8765, 5432, 3210, 9876, 6543, 4321, 7890]
    }
    return pd.DataFrame(data)