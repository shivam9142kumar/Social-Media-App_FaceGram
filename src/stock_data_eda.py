import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
file_path = "D:/stock_data.csv"
df = pd.read_csv(file_path)

# Data Cleaning and Basic Analysis
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

print("Dataframe Info:")
print(df.info())

print("Missing Values:")
print(df.isnull().sum())

print("\nDuplicate Entries:", df.duplicated().sum())

print("\nBasic Statistics:")
print(df.describe())

# Outlier detection using IQR method
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers

numerical_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']

for col in numerical_columns:
    outliers = detect_outliers_iqr(df, col)
    print(f"Outliers detected in {col}: {len(outliers)}")
    if not outliers.empty:
        print(outliers[[col,'stock']].head())

# Visualizations
plt.figure(figsize=(10, 6))
sns.boxplot(x='stock', y='Close', data=df)
plt.title('Boxplot of Closing Prices by Stock')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Close'], bins=50, kde=True)
plt.title('Distribution of Closing Prices')
plt.xlabel('Close Price')
plt.ylabel('Frequency')
plt.show()

# Correlation matrix and heatmap
plt.figure(figsize=(10, 8))
corr = df[numerical_columns].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Numerical Features')
plt.show()

# Time series plot of closing prices for each stock
plt.figure(figsize=(12, 8))
for stock in df['stock'].unique():
    stock_data = df[df['stock'] == stock]
    plt.plot(stock_data.index, stock_data['Close'], label=stock)
plt.title('Closing Prices Over Time by Stock')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()

# Volume trends over time for each stock
plt.figure(figsize=(12, 8))
for stock in df['stock'].unique():
    stock_data = df[df['stock'] == stock]
    plt.plot(stock_data.index, stock_data['Volume'], label=stock)
plt.title('Volume Over Time by Stock')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.legend()
plt.show()

# Moving averages (20-day and 50-day) for closing price of each stock
plt.figure(figsize=(12, 8))
for stock in df['stock'].unique():
    stock_data = df[df['stock'] == stock].copy()
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    plt.plot(stock_data.index, stock_data['Close'], label=f'{stock} Close')
    plt.plot(stock_data.index, stock_data['MA20'], label=f'{stock} MA20')
    plt.plot(stock_data.index, stock_data['MA50'], label=f'{stock} MA50')
plt.title('Closing Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Pairplot for numerical features colored by stock
sns.pairplot(df.reset_index(), vars=numerical_columns, hue='stock', diag_kind='kde')
plt.suptitle('Pairplot of Numerical Features by Stock', y=1.02)
plt.show()
