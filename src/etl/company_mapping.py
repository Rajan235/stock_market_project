import os 

DOWNLOADS_DIR = "data/downloads"
 
# companies = [
#     {"company_code": "ADANIPORTS", "screener_id": "6594426"},
#     {"company_code": "ASIANPAINT", "screener_id": "6594812"},
#     {"company_code": "AXISBANK", "screener_id": "6594837"},
#     {"company_code": "ADANIENT", "screener_id": "6594425"},
#     {"company_code": "APOLLOHOSP", "screener_id": "6594634"},
#     {"company_code": "BAJAJ-AUTO", "screener_id": "6594849"},
#     {"company_code": "BAJFINANCE", "screener_id": "6594851"},
#     {"company_code": "BEL", "screener_id": "6595017"},
#     {"company_code": "BHARTIARTL", "screener_id": "6595023"},
#     {"company_code": "CIPLA", "screener_id": "6595253"},
#     {"company_code": "COALINDIA", "screener_id": "6595259"},
#     {"company_code": "DRREDDY", "screener_id": "6595620"},
#     {"company_code": "EICHERMOT", "screener_id": "6595636"},
#     {"company_code": "ETERNAL", "screener_id": "68088707"},
#     {"company_code": "GRASIM", "screener_id": "6596053"},
#     {"company_code": "HCLTECH", "screener_id": "6596236"},
#     {"company_code": "HDFCBANK", "screener_id": "6596237"},
#     {"company_code": "HDFCLIFE", "screener_id": "17832651"},
#     {"company_code": "HEROMOTOCO", "screener_id": "6596243"},
#     {"company_code": "HINDALCO", "screener_id": "6596253"},
#     {"company_code": "HINDUNILVR", "screener_id": "6596263"},
#     {"company_code": "ICICIBANK", "screener_id": "6596413"},
#     {"company_code": "INDUSINDBK", "screener_id": "9695129"},
#     {"company_code": "INFY", "screener_id": "6596470"},
#     {"company_code": "ITC", "screener_id": "6596626"},
#     {"company_code": "JSWSTEEL", "screener_id": "6596816"},
#     {"company_code": "JIOFIN", "screener_id": "106186007"},
#     {"company_code": "KOTAKBANK", "screener_id": "6597025"},
#     {"company_code": "LT", "screener_id": "6597052"},
#     {"company_code": "M&M", "screener_id": "6597229"},
#     {"company_code": "MARUTI", "screener_id": "6597252"},
#     {"company_code": "NESTLEIND", "screener_id": "128275928"},
#     {"company_code": "NTPC", "screener_id": "6597657"},
#     {"company_code": "ONGC", "screener_id": "6597668"},
#     {"company_code": "POWERGRID", "screener_id": "6598025"},
#     {"company_code": "RELIANCE", "screener_id": "6598251"},
#     {"company_code": "SBILIFE", "screener_id": "17087873"},
#     {"company_code": "SHRIRAMFIN", "screener_id": "6598665"},
#     {"company_code": "SBIN", "screener_id": "6598877"},
#     {"company_code": "SUNPHARMA", "screener_id": "6599038"},
#     {"company_code": "TATACONSUM", "screener_id": "6599232"},
#     {"company_code": "TATAMOTORS", "screener_id": "6599235"},
#     {"company_code": "TATASTEEL", "screener_id": "6599238"},
#     {"company_code": "TRENT", "screener_id": "6599419"},
#     {"company_code": "TCS", "screener_id": "6599230"},
#     {"company_code": "TECHM", "screener_id": "6599866"},
#     {"company_code": "TITAN", "screener_id": "6599273"},
#     {"company_code": "ULTRACEMCO", "screener_id": "6599447"},
#     {"company_code": "WIPRO", "screener_id": "6599824"}
# ]

companies = [
    {"company_code": "ADANIPORTS", "screener_id": "6594426", "excel_file": "Adani Ports.xlsx"},
    {"company_code": "ASIANPAINT", "screener_id": "6594812", "excel_file": "Asian Paints.xlsx"},
    {"company_code": "AXISBANK", "screener_id": "6594837", "excel_file": "Axis Bank.xlsx"},
    {"company_code": "ADANIENT", "screener_id": "6594425", "excel_file": "Adani Enterp.xlsx"},
    {"company_code": "APOLLOHOSP", "screener_id": "6594634", "excel_file": "Apollo Hospitals.xlsx"},
    {"company_code": "BAJAJ-AUTO", "screener_id": "6594849", "excel_file": "Bajaj Auto.xlsx"},
    {"company_code": "BAJFINANCE", "screener_id": "6594851", "excel_file": "Bajaj Finance.xlsx"},
    {"company_code": "BEL", "screener_id": "6595017", "excel_file": "Bharat Electron.xlsx"},
    {"company_code": "BHARTIARTL", "screener_id": "6595023", "excel_file": "Bharti Airtel.xlsx"},
    {"company_code": "CIPLA", "screener_id": "6595253", "excel_file": "Cipla.xlsx"},
    {"company_code": "COALINDIA", "screener_id": "6595259", "excel_file": "Coal India.xlsx"},
    {"company_code": "DRREDDY", "screener_id": "6595620", "excel_file": "Dr Reddy's Labs.xlsx"},
    {"company_code": "EICHERMOT", "screener_id": "6595636", "excel_file": "Eicher Motors.xlsx"},
    {"company_code": "ETERNAL", "screener_id": "68088707", "excel_file": "Eternal Ltd.xlsx"},
    {"company_code": "GRASIM", "screener_id": "6596053", "excel_file": "Grasim Inds.xlsx"},
    {"company_code": "HCLTECH", "screener_id": "6596236", "excel_file": "HCL Technologies.xlsx"},
    {"company_code": "HDFCBANK", "screener_id": "6596237", "excel_file": "HDFC Bank.xlsx"},
    {"company_code": "HDFCLIFE", "screener_id": "17832651", "excel_file": "HDFC Life Insur.xlsx"},
    {"company_code": "HEROMOTOCO", "screener_id": "6596243", "excel_file": "Hero Motocorp.xlsx"},
    {"company_code": "HINDALCO", "screener_id": "6596253", "excel_file": "Hindalco Inds.xlsx"},
    {"company_code": "HINDUNILVR", "screener_id": "6596263", "excel_file": "Hind. Unilever.xlsx"},
    {"company_code": "ICICIBANK", "screener_id": "6596413", "excel_file": "ICICI Bank.xlsx"},
    {"company_code": "INDUSINDBK", "screener_id": "9695129", "excel_file": "IndusInd Bank.xlsx"},
    {"company_code": "INFY", "screener_id": "6596470", "excel_file": "Infosys.xlsx"},
    {"company_code": "ITC", "screener_id": "6596626", "excel_file": "ITC.xlsx"},
    {"company_code": "JSWSTEEL", "screener_id": "6596816", "excel_file": "JSW Steel.xlsx"},
    {"company_code": "JIOFIN", "screener_id": "106186007", "excel_file": "Jio Financial.xlsx"},
    {"company_code": "KOTAKBANK", "screener_id": "6597025", "excel_file": "Kotak Mah. Bank.xlsx"},
    {"company_code": "LT", "screener_id": "6597052", "excel_file": "Larsen & Toubro.xlsx"},
    {"company_code": "M&M", "screener_id": "6597229", "excel_file": "M & M.xlsx"},
    {"company_code": "MARUTI", "screener_id": "6597252", "excel_file": "Maruti Suzuki.xlsx"},
    {"company_code": "NESTLEIND", "screener_id": "128275928", "excel_file": "Nestle India.xlsx"},
    {"company_code": "NTPC", "screener_id": "6597657", "excel_file": "NTPC.xlsx"},
    {"company_code": "ONGC", "screener_id": "6597668", "excel_file": "O N G C.xlsx"},
    {"company_code": "POWERGRID", "screener_id": "6598025", "excel_file": "Power Grid Corpn.xlsx"},
    {"company_code": "RELIANCE", "screener_id": "6598251", "excel_file": "Reliance Industr.xlsx"},
    {"company_code": "SBILIFE", "screener_id": "17087873", "excel_file": "SBI Life Insuran.xlsx"},
    {"company_code": "SHRIRAMFIN", "screener_id": "6598665", "excel_file": "Shriram Finance.xlsx"},
    {"company_code": "SBIN", "screener_id": "6598877", "excel_file": "St Bk of India.xlsx"},
    {"company_code": "SUNPHARMA", "screener_id": "6599038", "excel_file": "Sun Pharma.Inds.xlsx"},
    {"company_code": "TATACONSUM", "screener_id": "6599232", "excel_file": "Tata Consumer.xlsx"},
    {"company_code": "TATAMOTORS", "screener_id": "6599235", "excel_file": "Tata Motors.xlsx"},
    {"company_code": "TATASTEEL", "screener_id": "6599238", "excel_file": "Tata Steel.xlsx"},
    {"company_code": "TRENT", "screener_id": "6599419", "excel_file": "Trent.xlsx"},
    {"company_code": "TCS", "screener_id": "6599230", "excel_file": "TCS.xlsx"},
    {"company_code": "TECHM", "screener_id": "6599866", "excel_file": "Tech Mahindra.xlsx"},
    {"company_code": "TITAN", "screener_id": "6599273", "excel_file": "Titan Company.xlsx"},
    {"company_code": "ULTRACEMCO", "screener_id": "6599447", "excel_file": "UltraTech Cem.xlsx"},
    {"company_code": "WIPRO", "screener_id": "6599824", "excel_file": "Wipro.xlsx"}
]

# companies = [
#      {"company_code": "ADANIPORTS", "screener_id": "6594426", "excel_file": "Adani Ports.xlsx"},
# ]

# def add_excel_filenames(companies, downloads_dir=DOWNLOADS_DIR):
#     files = os.listdir(downloads_dir)
#     files_lower = {f.lower(): f for f in files}  # for case-insensitive matching

#     for company in companies:
#         # Try to find a file that starts with the company code (case-insensitive)
#         code = company["company_code"].lower()
#         excel_file = None
#         for f in files:
#             if f.lower().startswith(code) and f.lower().endswith('.xlsx'):
#                 excel_file = f
#                 break
#         if excel_file:
#             company["excel_file"] = os.path.join(downloads_dir, excel_file)
#         else:
#             company["excel_file"] = None  # or leave out the key, or log a warning

# add_excel_filenames(companies)

# # Example: print companies with their Excel file
# for c in companies:
#     print(c)