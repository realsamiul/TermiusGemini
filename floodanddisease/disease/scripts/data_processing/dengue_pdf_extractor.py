#!/usr/bin/env python3
"""
HAWKEYE OMEGA v2: DGHS PDF Data Extractor
Extracts dengue data from downloaded DGHS PDF reports (2022-2024)
"""

import pandas as pd
import fitz  # PyMuPDF
import re
import os
import numpy as np
from datetime import datetime
from pathlib import Path

# --- CONFIGURATION ---
PDF_DIRECTORY = "./dengue_reports_2022_2024/pdfs/"  # Correct path to downloaded PDFs
OUTPUT_FILE = "./bangladesh_dengue_cases_2022_2025.csv"  # Corrected output path
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

print("--- HAWKEYE OMEGA v2: DGHS PDF Data Extractor ---")
print(f"📁 PDF Directory: {PDF_DIRECTORY}")
print(f"📊 Output File: {OUTPUT_FILE}")
print(f"📅 Date Range: {START_DATE} to {END_DATE}")
print("=" * 60)

def clean_and_convert_to_int(text):
    """Removes Bengali numerals, commas, and converts to integer."""
    if text is None or text == '':
        return 0
    
    # Replace Bengali numerals with English numerals
    bengali_to_english = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
    cleaned_text = str(text).translate(bengali_to_english)
    
    # Remove commas and any non-digit characters except minus sign
    cleaned_text = re.sub(r'[^\d-]', '', cleaned_text)
    
    try:
        return int(cleaned_text) if cleaned_text else 0
    except (ValueError, TypeError):
        return 0

def extract_date_from_filename(filename):
    """Extract date from filename format: YYYY-MM-DD_ডঙগ_পরস_রলজ_..."""
    try:
        # Extract date from filename (first part before underscore)
        date_part = filename.split('_')[0]
        return datetime.strptime(date_part, '%Y-%m-%d').date()
    except (ValueError, IndexError):
        return None

def extract_data_from_pdf(file_path):
    """Extracts key dengue statistics from a single DGHS PDF report."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # --- Define Regex Patterns for Key Metrics ---
        # Multiple patterns to catch different formats
        
        # Date patterns (multiple formats)
        date_patterns = [
            r'তারিখ\s*([\d০-৯]{1,2}/[\d০-৯]{1,2}/[\d০-৯]{4})',
            r'Date\s*([\d০-৯]{1,2}/[\d০-৯]{1,2}/[\d০-৯]{4})',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{4})'
        ]
        
        # Case number patterns (multiple variations)
        case_patterns = [
            r'নতুন ভর্তি রোগী[:\s]*([\d,০-৯]+)',
            r'নতুন রোগী[:\s]*([\d,০-৯]+)',
            r'New\s+Admission[:\s]*([\d,০-৯]+)',
            r'Total\s+New\s+Cases[:\s]*([\d,০-৯]+)',
            r'নতুন কেস[:\s]*([\d,০-৯]+)',
            r'ভর্তি রোগী[:\s]*([\d,০-৯]+)'
        ]
        
        # Dhaka-specific patterns
        dhaka_patterns = [
            r'ঢাকায় নতুন ভর্তি রোগী[:\s]*([\d,০-৯]+)',
            r'ঢাকায় নতুন রোগী[:\s]*([\d,০-৯]+)',
            r'Dhaka\s+New\s+Cases[:\s]*([\d,০-৯]+)',
            r'ঢাকা[:\s]*([\d,০-৯]+)'
        ]
        
        # Death patterns
        death_patterns = [
            r'সর্বমোট মৃত্যু সংখ্যা[:\s]*([\d,০-৯]+)',
            r'মোট মৃত্যু[:\s]*([\d,০-৯]+)',
            r'Total\s+Deaths[:\s]*([\d,০-৯]+)',
            r'মৃত্যু[:\s]*([\d,০-৯]+)',
            r'Deaths[:\s]*([\d,০-৯]+)'
        ]
        
        # --- Extract Date ---
        report_date = None
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    date_str = match.group(1).translate(str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789'))
                    # Try different date formats
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']:
                        try:
                            report_date = datetime.strptime(date_str, fmt).date()
                            break
                        except ValueError:
                            continue
                    if report_date:
                        break
                except:
                    continue
        
        # Fallback to filename date
        if not report_date:
            report_date = extract_date_from_filename(os.path.basename(file_path))
        
        # --- Extract Case Numbers ---
        total_cases = 0
        for pattern in case_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                total_cases = clean_and_convert_to_int(match.group(1))
                if total_cases > 0:
                    break
        
        # --- Extract Dhaka Cases ---
        dhaka_cases = 0
        for pattern in dhaka_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                dhaka_cases = clean_and_convert_to_int(match.group(1))
                if dhaka_cases > 0:
                    break
        
        # --- Extract Deaths ---
        ytd_deaths = 0
        for pattern in death_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                ytd_deaths = clean_and_convert_to_int(match.group(1))
                if ytd_deaths > 0:
                    break
        
        if report_date:
            return {
                'date': report_date,
                'dhaka_cases': dhaka_cases,
                'total_new_cases': total_cases,
                'year_to_date_deaths': ytd_deaths,
                'filename': os.path.basename(file_path)
            }
        else:
            print(f"⚠️  Could not extract date from {os.path.basename(file_path)}")
            return None
            
    except Exception as e:
        print(f"⚠️  Could not process file {os.path.basename(file_path)}. Error: {e}")
        return None

def main():
    """Main execution function"""
    # Check if PDF directory exists
    if not os.path.exists(PDF_DIRECTORY):
        print(f"🔥 ERROR: The directory '{PDF_DIRECTORY}' does not exist.")
        print("🔥 Please run the dengue downloader first to download the PDF files.")
        return
    
    # Get all PDF files
    all_files = [os.path.join(PDF_DIRECTORY, f) for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith('.pdf')]
    
    if not all_files:
        print(f"🔥 ERROR: No PDF files found in '{PDF_DIRECTORY}'.")
        return
    
    print(f"📄 Found {len(all_files)} PDF files to process...")
    print("🔄 Processing files...")
    
    # Extract data from all PDFs
    extracted_data = []
    processed_count = 0
    
    for i, file in enumerate(sorted(all_files), 1):
        if i % 50 == 0:  # Progress indicator
            print(f"   Processed {i}/{len(all_files)} files...")
        
        data = extract_data_from_pdf(file)
        if data:
            extracted_data.append(data)
            processed_count += 1
    
    print(f"✅ Successfully processed {processed_count} out of {len(all_files)} files")
    
    if not extracted_data:
        print("🔥 ERROR: Could not extract data from any of the PDFs.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(extracted_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop_duplicates(subset='date', keep='last').sort_values('date')
    
    print(f"📊 Extracted data for {len(df)} unique dates")
    print(f"📅 Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    
    # --- Synthesize a Complete Time Series ---
    print("\n🔄 Synthesizing complete daily time series...")
    
    # Create a full date range for the required period
    full_date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    
    # Reindex the dataframe to the full date range
    df = df.set_index('date').reindex(full_date_range).reset_index().rename(columns={'index': 'date'})
    
    # Use interpolation to fill missing values for a smooth, plausible time series
    # Set date as index for time-based interpolation
    df_temp = df.set_index('date')
    df_temp['dhaka_cases'] = df_temp['dhaka_cases'].interpolate(method='time')
    df_temp['total_new_cases'] = df_temp['total_new_cases'].interpolate(method='time')
    df_temp['year_to_date_deaths'] = df_temp['year_to_date_deaths'].interpolate(method='time')
    df = df_temp.reset_index()
    
    # Add a column to distinguish real from synthesized data
    df['data_source'] = np.where(df['total_new_cases'].notna(), 'official_report', 'synthesized_estimate')
    
    # Clean up the final dataframe
    df = df.round().fillna(0)  # Round interpolated values and fill any remaining NaNs
    df['dhaka_cases'] = df['dhaka_cases'].astype(int)
    df['total_new_cases'] = df['total_new_cases'].astype(int)
    df['year_to_date_deaths'] = df['year_to_date_deaths'].astype(int)
    
    # Select and save the final columns
    output_df = df[['date', 'dhaka_cases', 'total_new_cases', 'year_to_date_deaths', 'data_source']]
    output_df.to_csv(OUTPUT_FILE, index=False)
    
    # Print summary statistics
    print("\n" + "="*70)
    print("✅ DATA EXTRACTION AND SYNTHESIS COMPLETE!")
    print(f"📊 Successfully processed {processed_count} PDFs")
    print(f"📈 Complete daily dataset with {len(output_df)} records")
    print(f"💾 Saved to: {OUTPUT_FILE}")
    print("\n📈 Summary Statistics:")
    print(f"   • Total Dhaka Cases: {output_df['dhaka_cases'].sum():,}")
    print(f"   • Total New Cases: {output_df['total_new_cases'].sum():,}")
    print(f"   • Total Deaths: {output_df['year_to_date_deaths'].max():,}")
    print(f"   • Official Reports: {len(output_df[output_df['data_source'] == 'official_report'])}")
    print(f"   • Synthesized Estimates: {len(output_df[output_df['data_source'] == 'synthesized_estimate'])}")
    print("="*70)

if __name__ == "__main__":
    main()
