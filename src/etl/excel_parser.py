import pandas as pd



def parse_financial_excel(file_path):
    df = pd.read_excel(file_path, sheet_name="Data Sheet", header=None)

    # Step 1: Locate all the 'Report Date' section headers
    section_indices = [14, 39, 54, 79]
    section_names = ["Profit & Loss", "Quarterly", "Balance Sheet", "Cash Flow"]
    # Step 2: Prepare dictionary to hold all cleaned sections
    all_sections = {}

    for i, start_idx in enumerate(section_indices):
        end_idx = section_indices[i + 1] if i + 1 < len(section_indices) else len(df)
        block = df.iloc[start_idx:end_idx].copy()
        section_name = section_names[i]
        #print(block)

        # Extract year/date headers from first row
        year_headers = block.iloc[1, 1:].tolist()
    #print (year_headers)
        # 2. Normalize headers to safe date strings
        years = [
            pd.to_datetime(str(y), errors="coerce").strftime("%Y-%m-%d") if pd.notna(pd.to_datetime(str(y), errors="coerce")) else f"Year_{j}"
            for j, y in enumerate(year_headers, 1)
        ]
        #print(years)

        # Prepare metrics table
        metric_df = block.iloc[2:].copy()
        metric_df.columns = ['metric'] + years
        metric_df.dropna(subset=['metric'], inplace=True)
        #metric_df['section'] = section_name
        #print(metric_df)

        # Transpose and format
        formatted = metric_df.set_index('metric').T
        formatted.index.name = 'year'
        formatted.reset_index(inplace=True)
        formatted.insert(0, 'section', section_name)
        #print(formatted)

        all_sections[section_name] = formatted

    # Example: Access structured profit & loss table
    #pl_section = all_sections.get("Balance Sheet")  # You can rename or map based on order or actual label
    #print(pl_section)

    # Reuse annual year headers from Profit & Loss
    annual_years = all_sections["Balance Sheet"]['year'].tolist()

    # Extract Price row
    price_row = df.iloc[89, 1:len(annual_years)+1].tolist()  # Row 89 is PRICE row
    price_df = pd.DataFrame({
        'section': ['Price'] * len(annual_years),
        'year': annual_years,
        'price': price_row
    })
    all_sections["Price"] = price_df

    #print(all_sections["Price"])
    # Extract derived row
    derived_label = df.iloc[92, 0]  # Should be: 'Adjusted Equity Shares in Cr'
    derived_row = df.iloc[92, 1:len(annual_years)+1].tolist()
    derived_df = pd.DataFrame({
        'section': ['Derived'] * len(annual_years),
        'year': annual_years,
        derived_label: derived_row
    })
    all_sections["Derived"] = derived_df
    
    return all_sections

    #print(all_sections["Derived"])

