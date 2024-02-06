import pandas as pd

# Read CSV with '$' separator
input_csv_path = 'input_file.csv'
df = pd.read_csv('knowledge-1707176676.csv', sep='$')

# Write to a new CSV with a standard separator (e.g., comma)
output_csv_path = 'output_file.csv'
df.to_csv(output_csv_path, index=False)

print(f'Data has been successfully read from {input_csv_path} and written to {output_csv_path}.')
