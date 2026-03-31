"""SEBI Insider & Bulk Deal Scanner."""
import pandas as pd
from typing import Any
from core.data_sources import NSESessionFetcher
from core.formatters import format_table, format_crores

KNOWN_FIIS = ["GOLDMAN SACHS", "MORGAN STANLEY", "JPMORGAN", "CITIGROUP", "CLSA", "NOMURA", "BARCLAYS", "HSBC", "DEUTSCHE", "UBS", "BNP PARIBAS", "SOCIETE GENERALE", "CREDIT SUISSE", "MACQUARIE"]
KNOWN_DIIS = ["LIC OF INDIA", "SBI MUTUAL FUND", "HDFC MUTUAL FUND", "ICICI PRUDENTIAL", "KOTAK MUTUAL", "NIPPON INDIA", "AXIS MUTUAL FUND", "UTI MUTUAL FUND", "ADITYA BIRLA"]
KNOWN_PROMOTERS = ["MUKESH AMBANI", "GAUTAM ADANI", "AZIM PREMJI", "RATAN TATA", "KUMAR MANGALAM BIRLA", "CYRUS MISTRY", "DILIP SHANGHVI", "UDAY KOTAK", "SHIV NADAR", "NARAYANA MURTHY", "NANDAN NILEKANI", "KIRAN MAZUMDAR"]

def classify_entity(name):
    name_upper = name.upper()
    for fii in KNOWN_FIIS:
        if fii in name_upper: return "FII"
    for dii in KNOWN_DIIS:
        if dii in name_upper: return "DII"
    for promoter in KNOWN_PROMOTERS:
        if promoter in name_upper: return "Promoter/HNI"
    corporate_keywords = ["LIMITED", "LTD", "FUND", "CAPITAL", "SECURITIES", "INVESTMENTS", "PVT", "LLC"]
    if any(kw in name_upper for kw in corporate_keywords): return "Unknown"
    # Single-word names without corporate keywords default to Unknown (insufficient info)
    words = name_upper.split()
    if len(words) <= 1: return "Unknown"
    return "Unknown"

def detect_patterns(deals):
    patterns = []
    if "buyer" in deals.columns:
        buyer_counts = deals["buyer"].value_counts()
        for buyer, count in buyer_counts.items():
            if count >= 2: patterns.append(f"Repeated buying by {buyer} ({count} deals)")
    if "symbol" in deals.columns and "value_cr" in deals.columns:
        by_symbol = deals.groupby("symbol")["value_cr"].sum()
        for sym, total in by_symbol.items():
            if total > 50: patterns.append(f"Large accumulation in {sym}: {format_crores(total * 10000000)}")
    return patterns

def compute_liquidity_impact(deal_value_cr, adtv_cr):
    if adtv_cr == 0: return 0.0
    return (deal_value_cr / adtv_cr) * 100

def run_deal_scanner(deal_type="all", period="1w", symbol=None, min_value=1.0):
    nse = NSESessionFetcher()
    raw = nse.get_bulk_deals()
    if raw is None: return {"data": pd.DataFrame(), "patterns": [], "summary": "NSE data unavailable."}
    deals_list = raw if isinstance(raw, list) else raw.get("data", [])
    records = []
    for deal in deals_list:
        records.append({"symbol": deal.get("symbol", ""), "deal_type": deal.get("dealType", "Bulk"), "buyer": deal.get("clientName", ""), "value_cr": float(deal.get("value", 0)) / 10000000, "quantity": deal.get("quantity", 0), "price": deal.get("price", 0), "date": deal.get("dealDate", "")})
    df = pd.DataFrame(records)
    if df.empty: return {"data": df, "patterns": [], "summary": "No deals found."}
    if symbol: df = df[df["symbol"] == symbol.upper()]
    if deal_type != "all": df = df[df["deal_type"].str.lower() == deal_type.lower()]
    df = df[df["value_cr"] >= min_value]
    if "buyer" in df.columns: df["entity_type"] = df["buyer"].apply(classify_entity)
    patterns = detect_patterns(df)
    return {"data": df, "patterns": patterns, "summary": f"Found {len(df)} deals."}
