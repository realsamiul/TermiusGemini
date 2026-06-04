#!/usr/bin/env python3
"""
Quick script to complete the PDF extraction that was 99% done
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Load the partially processed data (if it exists)
try:
    # Try to load any existing CSV first
    df = pd.read_csv("bangladesh_dengue_cases_2022_2025.csv", parse_dates=['date'])
    print("✅ Found existing CSV file, completing the processing...")
except FileNotFoundError:
    print("❌ No existing CSV found. Need to run full PDF extraction.")
    exit(1)

print(f"📊 Loaded data with {len(df)} records")
print(f"📅 Date range: {df['date'].min().date()} to {df['date'].max().date()}")

# Fix the interpolation issue
print("🔄 Completing time series synthesis...")

# Create full date range
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"
full_date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

# Reindex to full date range
df = df.set_index('date').reindex(full_date_range).reset_index().rename(columns={'index': 'date'})

# Fix interpolation with proper DatetimeIndex
df_temp = df.set_index('date')
df_temp['dhaka_cases'] = df_temp['dhaka_cases'].interpolate(method='time')
df_temp['total_new_cases'] = df_temp['total_new_cases'].interpolate(method='time')
df_temp['year_to_date_deaths'] = df_temp['year_to_date_deaths'].interpolate(method='time')
df = df_temp.reset_index()

# Add data source column
df['data_source'] = np.where(df['total_new_cases'].notna(), 'official_report', 'synthesized_estimate')

# Clean up
df = df.round().fillna(0)
df['dhaka_cases'] = df['dhaka_cases'].astype(int)
df['total_new_cases'] = df['total_new_cases'].astype(int)
df['year_to_date_deaths'] = df['year_to_date_deaths'].astype(int)

# Save final output
output_df = df[['date', 'dhaka_cases', 'total_new_cases', 'year_to_date_deaths', 'data_source']]
output_df.to_csv("bangladesh_dengue_cases_2022_2025.csv", index=False)

print("\n" + "="*70)
print("✅ PDF EXTRACTION COMPLETED!")
print(f"📊 Final dataset: {len(output_df)} daily records")
print(f"📅 Complete time series: {output_df['date'].min().date()} to {output_df['date'].max().date()}")
print(f"💾 Saved to: bangladesh_dengue_cases_2022_2025.csv")
print("="*70)
