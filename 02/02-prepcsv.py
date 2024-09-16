import os
import pandas as pd

# Read the CSV file with specified data types
csv_input=pd.read_csv(
    os.path.join(os.getcwd(),'./data/test-recsys-data-5000.csv'),
    dtype={
        'CompanyName':str,
        'State':str,
        'Industry':str,
        'Segment':str,
        'Product 1 Name':str,'Product 1 Performance':float,
        'Product 2 Name':str,'Product 2 Performance':float,
        'Product 3 Name':str,'Product 3 Performance':float,
        'Product 4 Name':str,'Product 4 Performance':float,
        'Product 5 Name':str,'Product 5 Performance':float,
        'Product 6 Name':str,'Product 6 Performance':float,
        'Product 7 Name':str,'Product 7 Performance':float,
        'Product 8 Name':str,'Product 8 Performance':float
        }
    )

# Convert each row to JSON
csv_input['json'] = csv_input.apply(lambda x: x.to_json(), axis=1)

# Calculate the average performance of the products, ignoring missing columns
performance_columns = [col for col in csv_input.columns if 'Performance' in col]
csv_input['performance'] = csv_input[performance_columns].mean(axis=1, skipna=True)
#csv_input['performance'] = csv_input[["Product 1 Performance","Product 2 Performance","Product 3 Performance","Product 4 Performance","Product 5 Performance","Product 6 Performance","Product 7 Performance","Product 8 Performance"]].mean(axis=1)

# Create a company profile column
cols=['State','Industry','Segment']
csv_input['prof'] = csv_input[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# Save the JSON data to a file
csv_input.to_json('02/data/output1.json', orient='records')