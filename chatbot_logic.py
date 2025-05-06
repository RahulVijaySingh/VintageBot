import pandas as pd

df = pd.read_csv("housing_ecr_properties.csv")

def filter_properties(property_type=None, location=None, budget=None):
    results = df.copy()
    
    if property_type:
        results = results[results['Type & Location'].str.contains(property_type, case=False, na=False)]
    if location:
        results = results[results['Title'].str.contains(location, case=False, na=False)]
    if budget:
        try:
            min_budget, max_budget = map(float, budget.replace('₹','').replace('Cr','').split('-'))
            def price_range_in_budget(price_str):
                try:
                    price_vals = price_str.replace('₹','').replace('Cr','').split('-')
                    low = float(price_vals[0].strip())
                    high = float(price_vals[1].strip()) if len(price_vals) > 1 else low
                    return low >= min_budget and high <= max_budget
                except:
                    return False
            results = results[results['Price'].apply(price_range_in_budget)]
        except:
            pass

    return results.head(3).to_dict(orient='records')  # limit 3 results
