import requests

API_KEY = ""
STOCK_NAME = "SEQUENT"
YEARS = ("Mar 2024", "Mar 2025")
def fetch_data(stock_name, stats):
    url = f"https://stock.indianapi.in/historical_stats?stock_name={stock_name}&stats={stats}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed for {stats} with status code {response.status_code}")
        return {}

def build_company_data(all_data, years=YEARS):
    company_data = {}
    yoy = all_data.get("yoy_results", {})
    bs = all_data.get("balancesheet", {})
    cf = all_data.get("cashflow", {})
    for year in years:
        sales = yoy.get("Sales", {}).get(year)
        expenses = yoy.get("Expenses", {}).get(year)
        net_income = yoy.get("Net Profit", {}).get(year)
        gross_profit = sales - expenses if sales is not None and expenses is not None else None
        company_data[year] = {
            "Net Income": net_income,
            "Total Assets": bs.get("Total Assets", {}).get(year),
            "Operating Cash Flow": cf.get("Cash from Operating Activity", {}).get(year),
            "Long-term Debt": bs.get("Borrowings", {}).get(year),
            "Current Assets": bs.get("Other Assets", {}).get(year),  # No explicit "Current Assets", using "Other Assets"
            "Current Liabilities": bs.get("Other Liabilities", {}).get(year),  # No explicit "Current Liabilities", using "Other Liabilities"
            "Equity Capital": bs.get("Equity Capital", {}).get(year),
            "Gross Profit": gross_profit,
            "Revenue": sales,
        }
    return company_data


def piotroski_score(data):
    # Sort years by year number
    years = sorted(data.keys(), key=lambda x: int(x.split()[-1]))
    prev, curr = years[0], years[1]
    score = 0

    # 1. Positive Net Income
    if data[curr]["Net Income"] is not None and data[curr]["Net Income"] > 0:
        score += 1

    # 2. Positive ROA
    if data[curr]["Net Income"] is not None and data[curr]["Total Assets"] not in (None, 0):
        roa_curr = data[curr]["Net Income"] / data[curr]["Total Assets"]
        if roa_curr > 0:
            score += 1
    else:
        roa_curr = None

    # 3. Positive Operating Cash Flow
    if data[curr]["Operating Cash Flow"] is not None and data[curr]["Operating Cash Flow"] > 0:
        score += 1

    # 4. Operating Cash Flow > Net Income
    if (data[curr]["Operating Cash Flow"] is not None and data[curr]["Net Income"] is not None and
        data[curr]["Operating Cash Flow"] > data[curr]["Net Income"]):
        score += 1

    # 5. Lower Leverage (Long-term Debt/Total Assets)
    if (data[curr]["Long-term Debt"] is not None and data[curr]["Total Assets"] not in (None, 0) and
        data[prev]["Long-term Debt"] is not None and data[prev]["Total Assets"] not in (None, 0)):
        leverage_curr = data[curr]["Long-term Debt"] / data[curr]["Total Assets"]
        leverage_prev = data[prev]["Long-term Debt"] / data[prev]["Total Assets"]
        if leverage_curr < leverage_prev:
            score += 1

    # 6. Higher Current Ratio (skip if missing)
    ca_curr = data[curr]["Current Assets"]
    cl_curr = data[curr]["Current Liabilities"]
    ca_prev = data[prev]["Current Assets"]
    cl_prev = data[prev]["Current Liabilities"]
    if None not in (ca_curr, cl_curr, ca_prev, cl_prev) and cl_curr != 0 and cl_prev != 0:
        curr_ratio_curr = ca_curr / cl_curr
        curr_ratio_prev = ca_prev / cl_prev
        if curr_ratio_curr > curr_ratio_prev:
            score += 1

    # 7. No new shares issued (Equity Capital unchanged or reduced)
    if (data[curr]["Equity Capital"] is not None and data[prev]["Equity Capital"] is not None and
        data[curr]["Equity Capital"] <= data[prev]["Equity Capital"]):
        score += 1

    # 8. Higher Gross Margin
    if (data[curr]["Gross Profit"] is not None and data[curr]["Revenue"] not in (None, 0) and
        data[prev]["Gross Profit"] is not None and data[prev]["Revenue"] not in (None, 0)):
        gross_margin_curr = data[curr]["Gross Profit"] / data[curr]["Revenue"]
        gross_margin_prev = data[prev]["Gross Profit"] / data[prev]["Revenue"]
        if gross_margin_curr > gross_margin_prev:
            score += 1

    # 9. Higher Asset Turnover
    if (data[curr]["Revenue"] not in (None, 0) and data[curr]["Total Assets"] not in (None, 0) and
        data[prev]["Revenue"] not in (None, 0) and data[prev]["Total Assets"] not in (None, 0)):
        asset_turnover_curr = data[curr]["Revenue"] / data[curr]["Total Assets"]
        asset_turnover_prev = data[prev]["Revenue"] / data[prev]["Total Assets"]
        if asset_turnover_curr > asset_turnover_prev:
            score += 1

    return score

if __name__ == "__main__":
    # Fetch all required data
    all_data = fetch_data(STOCK_NAME, "all")

    # Build company data
    company_data = build_company_data(all_data, YEARS)

    # Calculate Piotroski score
    score = piotroski_score(company_data)
    print("Piotroski F-Score:", score)