import pandas as pd 
import ast

df = pd.read_csv(r"C:\Users\NAVYA\Downloads\ESG\ESG_data_cleaned.csv")

# Remove rows with missing or NaN values in 'Esgscores'
df = df.dropna(subset=['Esgscores'])

# Apply literal_eval safely by skipping NaN values
df['Esgscores'] = df['Esgscores'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})

# Expand the ESG dictionary into separate columns
esg_expanded = df['Esgscores'].apply(pd.Series)

# Merge the expanded ESG data with the ticker column
final_df = pd.concat([df[['Ticker']], esg_expanded], axis=1)

# Drop irrelevant columns if needed
final_df.drop(columns=['maxAge'], inplace=True, errors='ignore')

# Save cleaned data to a new CSV file
final_df.to_csv("ESG_data_fixed.csv", index=False)

# Display first few rows of the cleaned data
print(final_df.head())
