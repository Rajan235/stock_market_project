def generate_signal(sales_growth, roce):
    if sales_growth is None or roce is None:
        return "No Data"
    if sales_growth > 10 and roce > 10:
        return "Buy"
    elif sales_growth < 0 or roce < 5:
        return "Sell"
    else:
        return "Hold"