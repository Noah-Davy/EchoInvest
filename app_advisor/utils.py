# utils.py
import pandas_market_calendars as mcal
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
from .models import Portfolio

# Alpha Vantage API key
api_key = 'V235L3PAVTJ14VXC'

# Define the risk scores for each response
risk_scores = {
    "q1": {"a": 4, "b": 3, "c": 2, "d": 1},
    "q2": {"a": 1, "b": 2, "c": 3, "d": 4},
    "q3": {"a": 1, "b": 2, "c": 3, "d": 4},
    "q4": {"a": 1, "b": 2, "c": 3},
    "q5": {"a": 1, "b": 2, "c": 3},
    "q6": {"a": 1, "b": 2, "c": 3, "d": 4},
    "q7": {"a": 1, "b": 2, "c": 3, "d": 4},
    "q8": {"a": 1, "b": 2, "c": 3, "d": 4},
    "q9": {"a": 1, "b": 3},
    "q10": {"a": 1, "b": 3},
    "q11": {"a": 1, "b": 2, "c": 3, "d": 4},
    "q12": {"a": 1, "b": 2, "c": 3},
    "q13": {"a": 1, "b": 2, "c": 3, "d": 4}
}

# Define the portfolios for each risk tolerance level
portfolios = {
    "High tolerance for risk": {
        "stocks": 80,
        "bonds": 15,
        "cash": 5
    },
    "Above-average tolerance for risk": {
        "stocks": 70,
        "bonds": 25,
        "cash": 5
    },
    "Average/moderate tolerance for risk": {
        "stocks": 60,
        "bonds": 35,
        "cash": 5
    },
    "Below-average tolerance for risk": {
        "stocks": 50,
        "bonds": 45,
        "cash": 5
    },
    "Low tolerance for risk": {
        "stocks": 30,
        "bonds": 60,
        "cash": 10
    }
}

# Define the individual stocks for each asset class
stocks = {
    "stocks": [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        # (other stock entries omitted for brevity)
    ],
    "bonds": [
        {"symbol": "VCIT", "name": "Vanguard Intermediate-Term Corporate Bond ETF"},
        # (other bond entries omitted for brevity)
    ],
    "cash": [
        {"symbol": "MINT", "name": "PIMCO Enhanced Short Maturity Active ETF"},
        # (other cash entries omitted for brevity)
    ]
}

country_mapping = {
    "SSNLF": "South Korea",
    "TSM": "Taiwan",
    # (other country mappings omitted for brevity)
}

# Function to calculate the risk score based on user responses
def calculate_risk_score(responses):
    total_score = 0
    for question, response in responses.items():
        total_score += risk_scores[question][response]
    return total_score

# Function to determine the risk tolerance level based on the risk score
def determine_risk_tolerance(score):
    if score >= 33 and score <= 47:
        return "High tolerance for risk"
    elif score >= 29 and score <= 32:
        return "Above-average tolerance for risk"
    elif score >= 23 and score <= 28:
        return "Average/moderate tolerance for risk"
    elif score >= 19 and score <= 22:
        return "Below-average tolerance for risk"
    else:
        return "Low tolerance for risk"

# Function to recommend a portfolio based on the risk tolerance level
def recommend_portfolio(risk_tolerance):
    return portfolios[risk_tolerance]

# Function to fetch company overview data
def fetch_company_overview(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to get the latest price with caching
def get_latest_price(symbol, cache_expiry=3600):
    cache_file = f"{symbol}_cache.json"
    try:
        with open(cache_file, "r") as file:
            cache_data = json.load(file)
            if "timestamp" in cache_data and "price" in cache_data:
                cache_timestamp = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now() - cache_timestamp < timedelta(seconds=cache_expiry):
                    print(f"Using cached price for {symbol}: {cache_data['price']}")
                    return cache_data["price"]
    except FileNotFoundError:
        pass

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "Global Quote" in data and "05. price" in data["Global Quote"]:
        price = float(data["Global Quote"]["05. price"])
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "price": price
        }
        with open(cache_file, "w") as file:
            json.dump(cache_data, file)
        print(f"Retrieved latest price for {symbol}: {price}")
        return price
    else:
        print(f"Error retrieving price for {symbol}: {data}")
        return None

def get_historical_prices(symbol, start_date, end_date):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "Error Message" in data:
        print(f"Error retrieving data for {symbol}: {data['Error Message']}")
        return None

    prices = {}

    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        available_dates = sorted(time_series.keys(), reverse=True)

        for date in available_dates:
            if date <= end_date:
                if date >= start_date:
                    prices[date] = float(time_series[date]["5. adjusted close"])
                else:
                    break

    return prices

# Function to allocate the portfolio based on the recommended portfolio and initial investment
def allocate_portfolio(portfolio_allocation, initial_investment):
    allocated_portfolio = {
        "total_investment": initial_investment,
        "asset_classes": [],
        "region_allocation": {},
        "sector_allocation": {}
    }

    for asset_class, percentage in portfolio_allocation.items():
        asset_allocation = initial_investment * (percentage / 100)
        num_stocks = len(stocks[asset_class])
        stock_allocations = []
        for stock in stocks[asset_class]:
            stock_price = get_latest_price(stock["symbol"])

            if stock_price is None or stock_price == 0:
                print(f"Invalid stock price for {stock['symbol']}. Skipping allocation.")
                continue

            stock_allocation = asset_allocation / num_stocks
            stock_shares = stock_allocation / float(stock_price)

            print(f"Stock: {stock['symbol']}")
            print(f"Stock Price: {stock_price}")
            print(f"Stock Allocation: {stock_allocation}")
            print(f"Stock Shares: {stock_shares}")
            print("---")

            # Get the company overview data for sector and country allocation
            company_data = fetch_company_overview(stock["symbol"])

            if "Sector" in company_data:
                sector = company_data["Sector"]
                if sector in allocated_portfolio["sector_allocation"]:
                    allocated_portfolio["sector_allocation"][sector] += stock_allocation
                else:
                    allocated_portfolio["sector_allocation"][sector] = stock_allocation

            country = None
            if "Country" in company_data:
                country = company_data["Country"]
            elif stock["symbol"] in country_mapping:
                country = country_mapping[stock["symbol"]]

            if country:
                if country in allocated_portfolio["region_allocation"]:
                    allocated_portfolio["region_allocation"][country] += stock_allocation
                else:
                    allocated_portfolio["region_allocation"][country] = stock_allocation

            stock_allocations.append({
                "symbol": stock["symbol"],
                "name": stock["name"],
                "price": stock_price,
                "shares": stock_shares,
                "allocation": stock_allocation
            })
        allocated_portfolio["asset_classes"].append({
            "name": asset_class,
            "allocation": asset_allocation,
            "percentage": percentage,
            "stocks": stock_allocations
        })

    # Calculate the total allocation for each region and sector
    total_region_allocation = sum(allocated_portfolio["region_allocation"].values())
    total_sector_allocation = sum(allocated_portfolio["sector_allocation"].values())

    # Convert the region and sector allocations to percentages
    for region in allocated_portfolio["region_allocation"]:
        allocated_portfolio["region_allocation"][region] = allocated_portfolio["region_allocation"][region] / total_region_allocation * 100

    for sector in allocated_portfolio["sector_allocation"]:
        allocated_portfolio["sector_allocation"][sector] = allocated_portfolio["sector_allocation"][sector] / total_sector_allocation * 100

    return allocated_portfolio

def calculate_portfolio_performance(allocated_portfolio, initial_investment, end_date):
    portfolio_prices = {}
    start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=365*4)).strftime("%Y-%m-%d")  ####CHANGE YEAR HERE

    print(f"Initial Investment: {initial_investment}")

    spy_prices = get_historical_prices("SPY", start_date, end_date)  ####CHANGE COMPARISON HERE

    if spy_prices:
        spy_dates = sorted(spy_prices.keys())
        if spy_dates:
            spy_shares = initial_investment / spy_prices[spy_dates[0]]
            print(f"SPY Shares: {spy_shares}")
        else:
            print("No SPY historical prices available for the given date range. Skipping SPY performance calculation.")
            spy_shares = 0
    else:
        print("SPY historical prices not available. Skipping SPY performance calculation.")
        spy_shares = 0

    for asset_class in allocated_portfolio["asset_classes"]:
        for stock in asset_class["stocks"]:
            stock_prices = get_historical_prices(stock["symbol"], start_date, end_date)

            if stock_prices:
                stock_dates = sorted(stock_prices.keys())
                if stock_dates:
                    stock_shares = stock["allocation"] / stock_prices[stock_dates[0]]
                    print(f"Stock: {stock['symbol']}, Allocation: {stock['allocation']}, Initial Price: {stock_prices[stock_dates[0]]}, Shares: {stock_shares}")

                    for date in stock_prices:
                        if date not in portfolio_prices:
                            portfolio_prices[date] = 0
                        portfolio_prices[date] += stock_prices[date] * stock_shares
                else:
                    print(f"No historical prices available for {stock['symbol']} for the given date range. Skipping performance calculation for this stock.")
            else:
                print(f"Historical prices not available for {stock['symbol']}. Skipping performance calculation for this stock.")

    print(f"Portfolio Prices: {portfolio_prices}")

    sorted_dates = sorted(portfolio_prices.keys())

    if sorted_dates:
        portfolio_performance = []
        spy_performance = []

        for date in sorted_dates:
            if portfolio_prices[date] != 0:
                portfolio_performance.append(portfolio_prices[date])
                if date in spy_prices:
                    spy_performance.append(spy_prices[date] * spy_shares)
                else:
                    spy_performance.append(None)
    else:
        print("No historical price data available for the portfolio. Skipping performance calculation.")
        portfolio_performance = []
        spy_performance = []

    return {
        "start_date": start_date,
        "portfolio_performance": portfolio_performance,
        "spy_performance": spy_performance
    }

def get_previous_trading_day():
    # Load the trading calendar for NYSE
    nyse = mcal.get_calendar('NYSE')

    # Get today's date in the correct format
    today = datetime.now().strftime('%Y-%m-%d')

    # Find the last valid trading day
    valid_days = nyse.valid_days(start_date='2010-01-01', end_date=today)

    # Look for the previous trading day
    if len(valid_days) > 1:
        previous_trading_day = valid_days[-2]  # Gets the second to last valid day (yesterday or the last trading day)
    else:
        # This case handles if it's the first trading day of the year
        previous_trading_day = valid_days[-1]

    return previous_trading_day.strftime('%Y-%m-%d')

# Function to plot pie chart
def plot_pie_chart(data, title, filename=None):
    labels = list(data.keys())
    sizes = list(data.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)

    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def ensure_json_serializable(data):
    if isinstance(data, dict):
        return {key: ensure_json_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [ensure_json_serializable(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()  # Convert datetime to string
    elif isinstance(data, (int, float, str, bool)) or data is None:
        return data
    else:
        return str(data)  # Convert any other types to string

def save_portfolio(user, risk_score, risk_tolerance, allocated_portfolio, portfolio_performance):
    # Ensure the data is JSON-serializable
    allocated_portfolio = ensure_json_serializable(allocated_portfolio)
    portfolio_performance = ensure_json_serializable(portfolio_performance)

    Portfolio.objects.create(
        user=user,
        risk_score=risk_score,
        risk_tolerance=risk_tolerance,
        portfolio_data={
            'allocated_portfolio': allocated_portfolio,
            'portfolio_performance': portfolio_performance
        }
    )

def generate_allocation_charts(allocated_portfolio):
    # Generate and save region allocation pie chart
    region_allocation = allocated_portfolio['region_allocation']
    plot_pie_chart(region_allocation, 'Regional Allocation', 'static/region_allocation.png')

    # Generate and save sector allocation pie chart
    sector_allocation = allocated_portfolio['sector_allocation']
    plot_pie_chart(sector_allocation, 'Sector Allocation', 'static/sector_allocation.png')

def main(user, user_responses, initial_investment):
    # Calculate the risk score based on user responses
    risk_score = calculate_risk_score(user_responses)

    # Determine the risk tolerance level based on the risk score
    risk_tolerance = determine_risk_tolerance(risk_score)

    # Recommend a portfolio based on the risk tolerance level
    recommended_portfolio = recommend_portfolio(risk_tolerance)

    # Allocate the portfolio based on the recommended portfolio and initial investment
    allocated_portfolio = allocate_portfolio(recommended_portfolio, initial_investment)

    # Get the previous trading day
    end_date = get_previous_trading_day()

    # Calculate the portfolio performance over the last 10 years
    portfolio_performance = calculate_portfolio_performance(allocated_portfolio, initial_investment, end_date)

    # Generate and save allocation charts
    generate_allocation_charts(allocated_portfolio)

    # Save the portfolio to the database
    save_portfolio(user, risk_score, risk_tolerance, allocated_portfolio, portfolio_performance)

    return {
        'risk_score': risk_score,
        'risk_tolerance': risk_tolerance,
        'allocated_portfolio': allocated_portfolio,
        'portfolio_performance': portfolio_performance
    }
