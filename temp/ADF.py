from yahoo_fin.stock_info import get_data

def Company(__name__):

    if __name__ == "Amazon":
        amazon_daily = get_data("amzn", start_date="12/04/2017", end_date="12/04/2019", index_as_date = True, interval="1d")
        print(amazon_daily)

    if __name__ == "Google":
        google_daily = get_data("googl", start_date="12/04/2017", end_date="12/04/2019", index_as_date = True, interval="1d")
        print(google_daily)

print(Company("Amazon"))
print(Company("Google"))