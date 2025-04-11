import pandas as pd

# Part a) Downloaded data from FRED and converted to CSV
df = pd.read_csv("GDPC1.csv")

df.columns = ["Date", "GDP"]
df["Date"] = pd.to_datetime(df["Date"])

# Calc GDP Growth
df["GrowthRate"] = df["GDP"].pct_change() * 100 * 4

df.dropna(inplace=True)

print(df.head())

import matplotlib.pyplot as plt

# Create Plot for Growth Rate
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["GrowthRate"], color="blue", linewidth=1.5)
plt.title("U.S. Real GDP Growth (Quarterly, Annualized)")
plt.xlabel("Year")
plt.ylabel("Growth Rate (%)")
plt.grid(True)

plt.show()

# Part b) Mean: 3.09%, STD: 4.47%
mean_growth = df["GrowthRate"].mean()
std_growth = df["GrowthRate"].std()

print(f"Mean GDP Growth Rate: {mean_growth:.2f}%")
print(f"Standard Deviation of GDP Growth Rate: {std_growth:.2f}%")

# Part c) subsample 1: Mean: 3.31%, STD: 4.31%. subsample 2: Mean: 3.73%, STD: 2.26%. subsample 3: Mean: 2.13%, STD: 5.16%.
subsample1 = df[(df["Date"] >= "1960-01-01") & (df["Date"] <= "1982-12-31")]
subsample2 = df[(df["Date"] >= "1983-01-01") & (df["Date"] <= "2000-12-31")]
subsample3 = df[(df["Date"] >= "2001-01-01") & (df["Date"] <= "2024-12-31")]


stats = {
    "Period": ["1960:Q1-1982:Q4", "1983:Q1-2000:Q4", "2001:Q1-2024:Q4"],
    "Mean Growth Rate (%)": [
        subsample1["GrowthRate"].mean(),
        subsample2["GrowthRate"].mean(),
        subsample3["GrowthRate"].mean(),
    ],
    "Standard Deviation (%)": [
        subsample1["GrowthRate"].std(),
        subsample2["GrowthRate"].std(),
        subsample3["GrowthRate"].std(),
    ],
}


stats_df = pd.DataFrame(stats)
print(stats_df)

# d) The second subsample had the highest mean growth rate of 3.73% while the most recent (3rd subsample) had the lowest of 2.13%. The 2nd subsample had the lowest standard deviation while the 3rd subsample had the highest, most likely from the massive spikes of GDP from Covid

# 2. Wisconsin Unemployment Rate seems to follow for the most part the same trends as overall US Unemployment Rate. The main difference is Wisconsin tends to be under the US rate for the majority of the time. I believe this shows Wisconsin is a fairly stable employment state.

wi_unemployment = pd.read_csv("WIUR.csv")
us_unemployment = pd.read_csv("UNRATE.csv")

# Rename Data
wi_unemployment.rename(columns={"observation_date": "DATE", "WIUR": "Wisconsin_Unemployment"}, inplace=True)
us_unemployment.rename(columns={"observation_date": "DATE", "UNRATE": "US_Unemployment"}, inplace=True)
wi_unemployment["DATE"] = pd.to_datetime(wi_unemployment["DATE"])
us_unemployment["DATE"] = pd.to_datetime(us_unemployment["DATE"])
wi_unemployment.set_index("DATE", inplace=True)
us_unemployment.set_index("DATE", inplace=True)

# Resample to quarterly averages
wi_unemployment_quarterly = wi_unemployment.resample("Q").mean()
us_unemployment_quarterly = us_unemployment.resample("Q").mean()

# Filter data 
start_date = "1976-01-01"
end_date = "2024-12-31"
wi_unemployment_quarterly = wi_unemployment_quarterly.loc[start_date:end_date]
us_unemployment_quarterly = us_unemployment_quarterly.loc[start_date:end_date]

plt.figure(figsize=(12, 6))
plt.plot(wi_unemployment_quarterly.index, wi_unemployment_quarterly["Wisconsin_Unemployment"], label="Wisconsin Unemployment Rate", color="blue")
plt.plot(us_unemployment_quarterly.index, us_unemployment_quarterly["US_Unemployment"], label="U.S. Unemployment Rate", color="red")

plt.title("Quarterly Unemployment Rates: Wisconsin vs. U.S. (1976:Q1 - 2024:Q4)")
plt.xlabel("Year")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.grid(True)
plt.show()

#3. a) The SPF Forecast for 2025Q1 is an annual GDP growth of 1.9% (previously 1.8%) and unemployment rate of 4.1% (same as previous).
# Part b) The increase in GDP forecast would link to possible belief of economic expansion.

# Part c)
file_path = "Median_RGDP_Growth.xlsx"
df = pd.read_excel(file_path, sheet_name="Median_Growth")
df["Quarter"] = pd.to_datetime(df["YEAR"].astype(str) + "Q" + df["QUARTER"].astype(str))
df_filtered = df[(df["Quarter"] >= "2000-01-01") & (df["Quarter"] <= "2024-12-31")]

# Plot DRGDP2
plt.figure(figsize=(12, 6))
plt.plot(df_filtered["Quarter"], df_filtered["DRGDP2"], marker="o", linestyle="-", color="b", label="1Q Ahead Forecast")
plt.title("1-Quarter-Ahead Forecast of U.S. Real GDP Growth (2000:Q1 - 2024:Q4)")
plt.xlabel("Quarter")
plt.ylabel("Annualized GDP Growth Forecast (%)")
plt.legend()
plt.grid(True)
plt.show()

# Part d) The largest error in the sample occurred during 2020-07-01 as the forecast did not predict such a large GPD growth.
# Some reasons for this would be the government stimulus checks, loosened lock down protocols, and companies adjusting to remote work, giving people income to spend.
#FRED GDP Data
gdp_df = pd.read_csv("GDPC1.csv")

gdp_df.rename(columns={"observation_date": "Date", "GDPC1": "Real_GDP"}, inplace=True)
gdp_df["Date"] = pd.to_datetime(gdp_df["Date"])
gdp_df = gdp_df[(gdp_df["Date"] >= "2000-01-01") & (gdp_df["Date"] <= "2024-12-31")]
gdp_df["Actual_GDP_Growth"] = gdp_df["Real_GDP"].pct_change() * 100 * 4 
gdp_df.dropna(inplace=True)

# Part c's Information
spf_file_path = "Median_RGDP_Growth.xlsx"  
spf_df = pd.read_excel(spf_file_path)
spf_df["Date"] = pd.to_datetime(spf_df["YEAR"].astype(str) + "Q" + spf_df["QUARTER"].astype(str))
spf_df = spf_df[["Date", "DRGDP2"]]
spf_df.rename(columns={"DRGDP2": "Forecast_GDP_Growth"}, inplace=True)
spf_df = spf_df[(spf_df["Date"] >= "2000-01-01") & (spf_df["Date"] <= "2024-12-31")]

#Merge data
merged_df = pd.merge(gdp_df, spf_df, on="Date", how="inner")

plt.figure(figsize=(14, 7))
plt.plot(merged_df["Date"], merged_df["Actual_GDP_Growth"], label="Actual GDP Growth", color="blue", marker="o")
plt.plot(merged_df["Date"], merged_df["Forecast_GDP_Growth"], label="Forecasted GDP Growth", color="red", linestyle="--", marker="x")

plt.title("Actual vs. Forecasted U.S. Real GDP Growth (2000:Q1 - 2024:Q4)")
plt.xlabel("Year")
plt.ylabel("Annualized GDP Growth Rate (%)")
plt.legend()
plt.grid(True)
plt.show()

