#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("Oura Ring MCP Server")

# Get Oura API token from environment
OURA_ACCESS_TOKEN = os.environ.get("OURA_ACCESS_TOKEN")
OURA_API_BASE = "https://api.ouraring.com/v2/usercollection"

if not OURA_ACCESS_TOKEN:
    raise ValueError("OURA_ACCESS_TOKEN environment variable not set")


def make_oura_request(endpoint: str, start_date: str = None, end_date: str = None) -> dict:
    """Helper function to make authenticated requests to Oura API"""
    headers = {
        "Authorization": f"Bearer {OURA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    url = f"{OURA_API_BASE}/{endpoint}"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_today_date() -> str:
    """Get tomorrow's date in YYYY-MM-DD format (to ensure we capture most recent data)"""
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def get_date_n_days_ago(days: int) -> str:
    """Get date n days ago in YYYY-MM-DD format"""
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


# ============================================================================
# TREND DATA TOOLS (30-DAY HISTORICAL DATA)
# ============================================================================

@mcp.tool(description="Get sleep data for the last 30 days to compare baseline patterns and detect anomalies")
def get_sleep_trends(days: int = 30) -> dict:
    """Fetch sleep trends for the last N days"""
    start_date = get_date_n_days_ago(days)
    end_date = get_today_date()
    return make_oura_request("sleep", start_date=start_date, end_date=end_date)


@mcp.tool(description="Get readiness data for the last 30 days to understand readiness patterns and baselines")
def get_readiness_trends(days: int = 30) -> dict:
    """Fetch readiness trends for the last N days"""
    start_date = get_date_n_days_ago(days)
    end_date = get_today_date()
    return make_oura_request("daily_readiness", start_date=start_date, end_date=end_date)


@mcp.tool(description="Get activity data for the last 30 days to track activity patterns and progress")
def get_activity_trends(days: int = 30) -> dict:
    """Fetch activity trends for the last N days"""
    start_date = get_date_n_days_ago(days)
    end_date = get_today_date()
    return make_oura_request("daily_activity", start_date=start_date, end_date=end_date)


@mcp.tool(description="Get stress data for the last 30 days to identify stress patterns and trends")
def get_stress_trends(days: int = 30) -> dict:
    """Fetch stress trends for the last N days"""
    start_date = get_date_n_days_ago(days)
    end_date = get_today_date()
    return make_oura_request("daily_stress", start_date=start_date, end_date=end_date)


@mcp.tool(description="Get resilience data for the last 30 days to track recovery capacity over time")
def get_resilience_trends(days: int = 30) -> dict:
    """Fetch resilience trends for the last N days"""
    start_date = get_date_n_days_ago(days)
    end_date = get_today_date()
    return make_oura_request("daily_resilience", start_date=start_date, end_date=end_date)


@mcp.tool(description="Get VO2 max (cardio capacity) trends for the last 30 days to track fitness progression")
def get_vo2_max_trends(days: int = 30) -> dict:
    """Fetch VO2 max trends for the last N days"""
    start_date = get_date_n_days_ago(days)
    end_date = get_today_date()
    return make_oura_request("vO2_max", start_date=start_date, end_date=end_date)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting Oura Ring MCP server on {host}:{port}")
    print(f"Connected to Oura API with token: {OURA_ACCESS_TOKEN[:10]}...")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
