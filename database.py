import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules

# MySQL connection details
username = 'root'
password = 'your_password'
host = 'localhost'
database = 'retail_db'

# Create a MySQL connection
conn = mysql.connector.connect(
    host=host,
    user=username,
    password=password,
    database=database
)

# Step 1: Retrieve data from MySQL
query = "SELECT * FROM Invoices"
df = pd.read_sql(query, conn)

# Display the first few rows of the dataframe
print(df.head())

# Step 2: Data Cleaning and Preprocessing
# Convert date columns to datetime format
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])

# Handle missing values if necessary
print("Missing Values:\n", df.isnull().sum())

# Step 3: Feature Engineering
# Calculate TotalAmount if not already present
if 'TotalAmount' not in df.columns:
    df['TotalAmount'] = df['Sales'] * df['Quantity']

# Display the first few rows to check TotalAmount calculation
print(df[['State', 'Sales', 'Quantity', 'TotalAmount']].head())

# Step 4: Data Analysis

# Analysis 1: Total Sales by State
total_sales_by_state = df.groupby('State')['TotalAmount'].sum().reset_index()

# Sort by TotalAmount and get the top 5 states
top_5_states = total_sales_by_state.sort_values(by='TotalAmount', ascending=False).head(5)
top_5_states['TotalAmount'] = top_5_states['TotalAmount'] / 1e6  # Convert to millions
print(top_5_states)

# Visualization: Total Sales by Top 5 States
plt.figure(figsize=(12, 6))
sns.barplot(data=top_5_states, x='State', y='TotalAmount')

plt.title('Total Sales by Top 5 States')
plt.xlabel('State')
plt.ylabel('Total Sales (in millions)')
plt.xticks(rotation=45)
plt.show()

# Analysis 2: Top 5 Products by Total Sales
top_5_products = df.groupby('Product_Name')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False).head(5)
print("Top 5 Products by Total Sales:")
print(top_5_products)

# Visualization: Top 5 Products by Total Sales
plt.figure(figsize=(12, 6))
sns.barplot(data=top_5_products, x='Product_Name', y='TotalAmount')
plt.title('Top 5 Products by Total Sales')
plt.xlabel('Product Name')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# Analysis 3: Top 4 Years by Total Sales
df['Order_Year'] = df['Order_Date'].dt.year
top_4_years = df.groupby('Order_Year')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False).head(5)
print("Top 4 Years by Total Sales:")
print(top_4_years)

# Visualization: Top 4 Years by Total Sales
plt.figure(figsize=(12, 6))
sns.barplot(data=top_4_years, x='Order_Year', y='TotalAmount')
plt.title('Top 4 Years by Total Sales')
plt.xlabel('Order Year')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# RFM Analysis
current_date = df['Order_Date'].max() + pd.DateOffset(1)
rfm_df = df.groupby('Customer_ID').agg({
    'Order_Date': lambda x: (current_date - x.max()).days,
    'Order_ID': 'count',
    'TotalAmount': 'sum'
}).reset_index()

rfm_df.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
print("RFM Analysis:")
print(rfm_df.head())

# Adding RFM Segment
rfm_df['RFM_Segment'] = (
    rfm_df['Recency'].apply(lambda x: '1' if x <= rfm_df['Recency'].quantile(0.25) else ('2' if x <= rfm_df['Recency'].quantile(0.50) else ('3' if x <= rfm_df['Recency'].quantile(0.75) else '4'))) +
    rfm_df['Frequency'].apply(lambda x: '4' if x > rfm_df['Frequency'].quantile(0.75) else ('3' if x > rfm_df['Frequency'].quantile(0.50) else ('2' if x > rfm_df['Frequency'].quantile(0.25) else '1'))) +
    rfm_df['Monetary'].apply(lambda x: '4' if x > rfm_df['Monetary'].quantile(0.75) else ('3' if x > rfm_df['Monetary'].quantile(0.50) else ('2' if x > rfm_df['Monetary'].quantile(0.25) else '1')))
)

rfm_df['RFM_Score'] = rfm_df['RFM_Segment'].apply(lambda x: int(x[0]) + int(x[1]) + int(x[2]))
print("RFM Analysis with Segments:")
print(rfm_df.head())

# Export RFM analysis to CSV
rfm_df.to_csv('rfm_analysis.csv', index=False)

# Visualization: RFM Segments
plt.figure(figsize=(12, 6))
sns.scatterplot(data=rfm_df, x='Recency', y='Monetary', hue='RFM_Score', size='Frequency', sizes=(20, 200), alpha=0.7, palette='viridis')
plt.title('RFM Segments')
plt.xlabel('Recency (days)')
plt.ylabel('Monetary Value ($)')
plt.show()

# Export top 5 products to CSV
top_5_products.to_csv('top_5_products.csv', index=False)

# Export top 5 states to CSV
top_5_states.to_csv('top_5_states.csv', index=False)

# Export top 4 years to CSV
top_4_years.to_csv('top_4_years.csv', index=False)

# Step 5: Close the cursor and connection
conn.close()
