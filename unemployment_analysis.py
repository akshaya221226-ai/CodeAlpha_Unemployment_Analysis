# ============================================================
# TASK 2: UNEMPLOYMENT ANALYSIS WITH PYTHON
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. FILE NAMES
# ============================================================

file1 = "Unemployment in India.csv"
file2 = "Unemployment_Rate_upto_11_2020.csv"

print("=" * 70)
print("        UNEMPLOYMENT ANALYSIS WITH PYTHON")
print("=" * 70)


# ============================================================
# 2. CHECK FILES
# ============================================================

if not os.path.exists(file1):
    print("\nERROR: 'Unemployment in India.csv' not found.")
    print("Please put the CSV file in the same folder as this Python file.")
    exit()

if not os.path.exists(file2):
    print("\nERROR: 'Unemployment_Rate_upto_11_2020.csv' not found.")
    print("Please put the CSV file in the same folder as this Python file.")
    exit()


# ============================================================
# 3. LOAD DATASETS
# ============================================================

file1 = "unemployment in india.csv"
file2 = "unemployment_rate_upto_11_2020.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
print("\nDatasets loaded successfully!")


# ============================================================
# 4. DISPLAY ORIGINAL DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET 1 INFORMATION")
print("=" * 70)

print("\nDataset shape:")
print(df1.shape)

print("\nColumn names:")
print(df1.columns.tolist())

print("\nFirst 5 rows:")
print(df1.head())


print("\n" + "=" * 70)
print("DATASET 2 INFORMATION")
print("=" * 70)

print("\nDataset shape:")
print(df2.shape)

print("\nColumn names:")
print(df2.columns.tolist())

print("\nFirst 5 rows:")
print(df2.head())


# ============================================================
# 5. CLEAN DATASET 1
# ============================================================

print("\n" + "=" * 70)
print("DATA CLEANING - DATASET 1")
print("=" * 70)

# Remove spaces from column names
df1.columns = df1.columns.str.strip()

# Remove spaces from string columns
for column in df1.select_dtypes(include="object").columns:
    df1[column] = df1[column].str.strip()

# Count rows before cleaning
rows_before = len(df1)

# Remove completely empty rows
df1 = df1.dropna(how="all")

# Convert Date column
df1["Date"] = pd.to_datetime(
    df1["Date"],
    dayfirst=True,
    errors="coerce"
)

# Remove rows where important values are missing
df1 = df1.dropna(
    subset=[
        "Date",
        "Estimated Unemployment Rate (%)",
        "Estimated Employed",
        "Estimated Labour Participation Rate (%)"
    ]
)

# Convert numeric columns
numeric_columns1 = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)"
]

for column in numeric_columns1:
    df1[column] = pd.to_numeric(
        df1[column],
        errors="coerce"
    )

# Remove rows with invalid numeric values
df1 = df1.dropna(subset=numeric_columns1)

rows_after = len(df1)

print("\nRows before cleaning:", rows_before)
print("Rows after cleaning :", rows_after)
print("Rows removed        :", rows_before - rows_after)

print("\nMissing values after cleaning:")
print(df1.isnull().sum())


# ============================================================
# 6. BASIC STATISTICS - DATASET 1
# ============================================================

print("\n" + "=" * 70)
print("BASIC STATISTICS - DATASET 1")
print("=" * 70)

average_unemployment = df1[
    "Estimated Unemployment Rate (%)"
].mean()

average_employment = df1[
    "Estimated Employed"
].mean()

average_labour = df1[
    "Estimated Labour Participation Rate (%)"
].mean()

print(
    f"\nAverage Unemployment Rate: "
    f"{average_unemployment:.2f}%"
)

print(
    f"Average Estimated Employed: "
    f"{average_employment:,.0f}"
)

print(
    f"Average Labour Participation Rate: "
    f"{average_labour:.2f}%"
)


# ============================================================
# 7. RURAL VS URBAN ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RURAL VS URBAN ANALYSIS")
print("=" * 70)

area_analysis = (
    df1.groupby("Area")[
        "Estimated Unemployment Rate (%)"
    ]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage unemployment by area:")

for area, rate in area_analysis.items():
    print(f"{area}: {rate:.2f}%")


# ============================================================
# 8. MONTHLY UNEMPLOYMENT ANALYSIS
# ============================================================

monthly_unemployment = (
    df1.groupby("Date")[
        "Estimated Unemployment Rate (%)"
    ]
    .mean()
    .sort_index()
)

print("\n" + "=" * 70)
print("MONTHLY UNEMPLOYMENT RATE")
print("=" * 70)

for date, rate in monthly_unemployment.items():
    print(
        f"{date.strftime('%B %Y')}: "
        f"{rate:.2f}%"
    )


# ============================================================
# 9. COVID-19 ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("COVID-19 IMPACT ANALYSIS")
print("=" * 70)

# Before COVID
pre_covid = df1[
    df1["Date"] < "2020-04-01"
]

# COVID period
covid_period = df1[
    (df1["Date"] >= "2020-04-01") &
    (df1["Date"] <= "2020-06-30")
]

# After June 2020
post_covid = df1[
    df1["Date"] > "2020-06-30"
]

pre_covid_rate = pre_covid[
    "Estimated Unemployment Rate (%)"
].mean()

covid_rate = covid_period[
    "Estimated Unemployment Rate (%)"
].mean()

print(
    f"\nPre-COVID average unemployment: "
    f"{pre_covid_rate:.2f}%"
)

print(
    f"COVID period average unemployment: "
    f"{covid_rate:.2f}%"
)

increase_points = covid_rate - pre_covid_rate

percentage_increase = (
    increase_points / pre_covid_rate
) * 100

print(
    f"Increase: "
    f"{increase_points:.2f} percentage points"
)

print(
    f"Percentage increase: "
    f"{percentage_increase:.2f}%"
)


# ============================================================
# 10. FIND HIGHEST UNEMPLOYMENT
# ============================================================

print("\n" + "=" * 70)
print("HIGHEST UNEMPLOYMENT OBSERVATION")
print("=" * 70)

highest_index = df1[
    "Estimated Unemployment Rate (%)"
].idxmax()

highest_row = df1.loc[highest_index]

print(
    "\nRegion:",
    highest_row["Region"]
)

print(
    "Date:",
    highest_row["Date"].strftime("%d-%m-%Y")
)

print(
    "Area:",
    highest_row["Area"]
)

print(
    "Unemployment Rate:",
    f"{highest_row['Estimated Unemployment Rate (%)']:.2f}%"
)


# ============================================================
# 11. LOWEST UNEMPLOYMENT
# ============================================================

print("\n" + "=" * 70)
print("LOWEST UNEMPLOYMENT OBSERVATION")
print("=" * 70)

lowest_index = df1[
    "Estimated Unemployment Rate (%)"
].idxmin()

lowest_row = df1.loc[lowest_index]

print(
    "\nRegion:",
    lowest_row["Region"]
)

print(
    "Date:",
    lowest_row["Date"].strftime("%d-%m-%Y")
)

print(
    "Area:",
    lowest_row["Area"]
)

print(
    "Unemployment Rate:",
    f"{lowest_row['Estimated Unemployment Rate (%)']:.2f}%"
)


# ============================================================
# 12. TOP 10 REGIONS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 REGIONS WITH HIGHEST AVERAGE UNEMPLOYMENT")
print("=" * 70)

region_average = (
    df1.groupby("Region")[
        "Estimated Unemployment Rate (%)"
    ]
    .mean()
    .sort_values(ascending=False)
)

print(
    region_average.head(10).round(2)
)


# ============================================================
# 13. LABOUR PARTICIPATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("LABOUR PARTICIPATION ANALYSIS")
print("=" * 70)

monthly_labour = (
    df1.groupby("Date")[
        "Estimated Labour Participation Rate (%)"
    ]
    .mean()
    .sort_index()
)

print(
    "\nAverage labour participation rate:",
    f"{df1['Estimated Labour Participation Rate (%)'].mean():.2f}%"
)


# ============================================================
# 14. COVID IMPACT BY AREA
# ============================================================

print("\n" + "=" * 70)
print("COVID IMPACT: RURAL VS URBAN")
print("=" * 70)

df1["Period"] = np.where(
    df1["Date"] < "2020-04-01",
    "Pre-COVID",
    "COVID"
)

covid_area = (
    df1.groupby(
        ["Period", "Area"]
    )["Estimated Unemployment Rate (%)"]
    .mean()
    .round(2)
)

print("\n")
print(covid_area)


# ============================================================
# 15. DATASET 2 CLEANING
# ============================================================

print("\n" + "=" * 70)
print("DATA CLEANING - DATASET 2")
print("=" * 70)

df2.columns = df2.columns.str.strip()

for column in df2.select_dtypes(include="object").columns:
    df2[column] = df2[column].str.strip()

rows2_before = len(df2)

df2 = df2.dropna(how="all")

# Identify date column
date_column2 = None

possible_date_columns = [
    "Date",
    "date",
    "Month",
    "month"
]

for column in possible_date_columns:
    if column in df2.columns:
        date_column2 = column
        break

if date_column2 is not None:

    df2[date_column2] = pd.to_datetime(
        df2[date_column2],
        dayfirst=True,
        errors="coerce"
    )

# Find unemployment column
unemployment_column2 = None

for column in df2.columns:

    if "unemployment" in column.lower():

        unemployment_column2 = column
        break

if unemployment_column2 is not None:

    df2[unemployment_column2] = pd.to_numeric(
        df2[unemployment_column2],
        errors="coerce"
    )

    df2 = df2.dropna(
        subset=[unemployment_column2]
    )

rows2_after = len(df2)

print(
    "\nDataset 2 rows before cleaning:",
    rows2_before
)

print(
    "Dataset 2 rows after cleaning:",
    rows2_after
)

print(
    "Dataset 2 rows removed:",
    rows2_before - rows2_after
)


# ============================================================
# 16. DATASET 2 ANALYSIS
# ============================================================

if unemployment_column2 is not None:

    print("\n" + "=" * 70)
    print("DATASET 2 ANALYSIS")
    print("=" * 70)

    avg2 = df2[
        unemployment_column2
    ].mean()

    print(
        "\nAverage unemployment rate:",
        f"{avg2:.2f}%"
    )

    highest2_index = df2[
        unemployment_column2
    ].idxmax()

    highest2 = df2.loc[highest2_index]

    print(
        "\nHighest unemployment value:",
        f"{highest2[unemployment_column2]:.2f}%"
    )

    # Monthly analysis
    if date_column2 is not None:

        monthly2 = (
            df2.groupby(date_column2)[
                unemployment_column2
            ]
            .mean()
            .sort_index()
        )

        print(
            "\nMonthly unemployment rate:"
        )

        for date, rate in monthly2.items():

            print(
                f"{date.strftime('%B %Y')}: "
                f"{rate:.2f}%"
            )


# ============================================================
# 17. GRAPH 1 - MONTHLY UNEMPLOYMENT TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_unemployment.index,
    monthly_unemployment.values,
    marker="o"
)

plt.axvline(
    pd.Timestamp("2020-04-01"),
    linestyle="--",
    label="COVID-19 Period"
)

plt.title(
    "Monthly Unemployment Rate in India"
)

plt.xlabel("Date")

plt.ylabel(
    "Unemployment Rate (%)"
)

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "01_monthly_unemployment_trend.png",
    dpi=300
)

plt.close()


# ============================================================
# 18. GRAPH 2 - RURAL VS URBAN
# ============================================================

plt.figure(figsize=(8, 6))

area_analysis.plot(
    kind="bar"
)

plt.title(
    "Average Unemployment: Rural vs Urban"
)

plt.xlabel("Area")

plt.ylabel(
    "Average Unemployment Rate (%)"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "02_rural_vs_urban.png",
    dpi=300
)

plt.close()


# ============================================================
# 19. GRAPH 3 - TOP 10 REGIONS
# ============================================================

plt.figure(figsize=(10, 7))

top10 = region_average.head(10).sort_values()

top10.plot(
    kind="barh"
)

plt.title(
    "Top 10 Regions by Average Unemployment"
)

plt.xlabel(
    "Average Unemployment Rate (%)"
)

plt.ylabel("Region")

plt.tight_layout()

plt.savefig(
    "03_top_10_regions.png",
    dpi=300
)

plt.close()


# ============================================================
# 20. GRAPH 4 - LABOUR PARTICIPATION
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_labour.index,
    monthly_labour.values,
    marker="o"
)

plt.axvline(
    pd.Timestamp("2020-04-01"),
    linestyle="--",
    label="COVID-19 Period"
)

plt.title(
    "Labour Participation Rate Over Time"
)

plt.xlabel("Date")

plt.ylabel(
    "Labour Participation Rate (%)"
)

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "04_labour_participation.png",
    dpi=300
)

plt.close()


# ============================================================
# 21. GRAPH 5 - COVID COMPARISON
# ============================================================

covid_comparison = pd.DataFrame({
    "Pre-COVID": [pre_covid_rate],
    "COVID": [covid_rate]
})

plt.figure(figsize=(7, 6))

plt.bar(
    covid_comparison.columns,
    covid_comparison.iloc[0]
)

plt.title(
    "Unemployment Before and During COVID-19"
)

plt.xlabel("Period")

plt.ylabel(
    "Average Unemployment Rate (%)"
)

plt.tight_layout()

plt.savefig(
    "05_covid_impact.png",
    dpi=300
)

plt.close()


# ============================================================
# 22. SAVE CLEANED DATASET
# ============================================================

df1.to_csv(
    "cleaned_unemployment_india.csv",
    index=False
)

df2.to_csv(
    "cleaned_unemployment_rate_2020.csv",
    index=False
)


# ============================================================
# 23. CREATE TEXT REPORT
# ============================================================

with open(
    "unemployment_analysis_report.txt",
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "UNEMPLOYMENT ANALYSIS REPORT\n"
    )

    report.write(
        "=" * 60 + "\n\n"
    )

    report.write(
        "1. DATASET INFORMATION\n"
    )

    report.write(
        f"Original rows: {rows_before}\n"
    )

    report.write(
        f"Cleaned rows: {rows_after}\n"
    )

    report.write(
        f"Average unemployment rate: "
        f"{average_unemployment:.2f}%\n\n"
    )

    report.write(
        "2. RURAL VS URBAN\n"
    )

    for area, rate in area_analysis.items():

        report.write(
            f"{area}: {rate:.2f}%\n"
        )

    report.write(
        "\n3. COVID-19 IMPACT\n"
    )

    report.write(
        f"Pre-COVID average: "
        f"{pre_covid_rate:.2f}%\n"
    )

    report.write(
        f"COVID average: "
        f"{covid_rate:.2f}%\n"
    )

    report.write(
        f"Increase: "
        f"{increase_points:.2f} percentage points\n"
    )

    report.write(
        f"Percentage increase: "
        f"{percentage_increase:.2f}%\n\n"
    )

    report.write(
        "4. HIGHEST UNEMPLOYMENT\n"
    )

    report.write(
        f"Region: {highest_row['Region']}\n"
    )

    report.write(
        f"Date: "
        f"{highest_row['Date'].strftime('%d-%m-%Y')}\n"
    )

    report.write(
        f"Rate: "
        f"{highest_row['Estimated Unemployment Rate (%)']:.2f}%\n\n"
    )

    report.write(
        "5. TOP 10 REGIONS\n"
    )

    report.write(
        str(region_average.head(10).round(2))
    )

    report.write(
        "\n\n6. CONCLUSION\n"
    )

    report.write(
        "The analysis shows a significant increase in "
        "unemployment during the COVID-19 pandemic. "
        "Urban unemployment was higher than rural "
        "unemployment, and labour participation also "
        "changed during the pandemic. After the peak "
        "period, unemployment began to decline, "
        "indicating gradual economic recovery.\n"
    )


# ============================================================
# 24. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("                 ANALYSIS COMPLETED")
print("=" * 70)

print("\nFiles created:")

print("1. 01_monthly_unemployment_trend.png")
print("2. 02_rural_vs_urban.png")
print("3. 03_top_10_regions.png")
print("4. 04_labour_participation.png")
print("5. 05_covid_impact.png")
print("6. cleaned_unemployment_india.csv")
print("7. cleaned_unemployment_rate_2020.csv")
print("8. unemployment_analysis_report.txt")

print("\nYour Task 2 analysis is complete!")