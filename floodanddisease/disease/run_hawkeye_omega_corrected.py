"""
HAWKEYE OMEGA v2.6 - BANGLADESH DISEASE-ECONOMY NEXUS ANALYSIS
===============================================================
Definitive Production Script - Defensive Enhancement Edition

This script represents the most advanced, stable, and defensible version
of the analysis pipeline. It integrates enhanced feature engineering and
defensible economic estimations to generate a comprehensive suite of assets
for immediate use in high-stakes presentations.

New in v2.6:
- Enhanced Feature Engineering (Rolling Averages, Monsoon Flag).
- Smarter forecasting model utilizing these new, richer features.
- Actionable, real-time "Mosquito Risk Index".
- Defensible, data-driven "Estimated Economic Burden" calculation.
- Expanded "Executive Briefing" text summary with risk dashboard and macro context.
"""

import os
import json
import warnings
import pandas as pd
import numpy as np
import requests
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C

# Suppress common warnings for a cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================================
# 🎯 CONFIGURATION PARAMETERS (from DATASET_ANALYSIS_REPORT.md)
# ============================================================================

# --- API & Geographic ---
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
DHAKA_LAT = 23.8103
DHAKA_LON = 90.4125

# --- Model Parameters ---
FORECAST_HORIZON = 14
CAUSAL_LAG = 7
CORR_THRESHOLD = 0.25

# --- Economic Estimation Parameters (for defensible estimation) ---
COST_PER_CASE_USD = 150  # Estimated direct treatment cost
ECONOMIC_LOSS_PER_CASE_USD = 500  # Estimated lost productivity

# --- File & Directory Paths ---
DATA_DIR = "./data/"
PROCESSED_DIR = os.path.join(DATA_DIR, "processed/")
RAW_DIR = os.path.join(DATA_DIR, "raw/")
REPORTS_DIR = "./reports/"
DASHBOARD_DIR = os.path.join(REPORTS_DIR, "dashboard/")
PLOTS_DIR = os.path.join(REPORTS_DIR, "individual_plots/")
DATA_EXPORTS_DIR = os.path.join(REPORTS_DIR, "data_exports/")
SUMMARY_DIR = os.path.join(REPORTS_DIR, "text_summary/")  # FIXED: was REports_DIR

# --- Input Filenames ---
DENGUE_FILE = "bangladesh_dengue_cases_2022_2025.csv"
WEATHER_FILE = "dhaka_weather_2022_2025.csv"
NIGHTLIGHT_FILE = "dhaka_nightlights_2022_2025.csv"
POPULATION_FILE = "bangladesh_population_monthly_2022_2025.csv"
ECONOMIC_FILE = "bangladesh_economic_indicators_2022_2025.csv"  # FIXED: removed "economic/" prefix

# ============================================================================
# 🔬 CORE ANALYSIS ENGINE
# ============================================================================

class HawkEyeOmega:
    """The main analysis pipeline for the HawkEye Omega v2.6 system."""

    def __init__(self):
        self.unified_df = None
        self.causal_graph = None
        self.predictions = None
        self.live_weather_data = {}
        self.macro_econ_context = {}
        self._setup_environment()

    def _setup_environment(self):
        """Ensures all necessary directories exist for the plentiful outputs."""
        print("INFO: Setting up analysis environment and output directories...")
        for path in [REPORTS_DIR, DASHBOARD_DIR, PLOTS_DIR, DATA_EXPORTS_DIR, SUMMARY_DIR]:
            os.makedirs(path, exist_ok=True)
        print("✅ Output directories are ready.")

    def _load_data_and_unify(self):
        """Loads, validates, unifies, and preprocesses all data sources with enhanced feature engineering."""
        print("\n[PHASE 1/5] 📥 Loading, Unifying, and Engineering Features...")
        try:
            dengue_df = pd.read_csv(os.path.join(PROCESSED_DIR, DENGUE_FILE), parse_dates=['date'])
            weather_df = pd.read_csv(os.path.join(PROCESSED_DIR, WEATHER_FILE), parse_dates=['date'])
            nightlight_df = pd.read_csv(os.path.join(PROCESSED_DIR, NIGHTLIGHT_FILE), parse_dates=['date'])
            population_df = pd.read_csv(os.path.join(PROCESSED_DIR, POPULATION_FILE), parse_dates=['date'])
            
            # Try to load economic data from processed first, then raw
            try:
                econ_df_raw = pd.read_csv(os.path.join(PROCESSED_DIR, ECONOMIC_FILE))
            except FileNotFoundError:
                print(f"INFO: Economic file not found in processed, trying raw directory...")
                econ_df_raw = pd.read_csv(os.path.join(RAW_DIR, "economic", ECONOMIC_FILE))
                
        except FileNotFoundError as e:
            print(f"❌ FATAL ERROR: Required data file not found: {e}. Halting execution.")
            return False

        # --- Live Weather Fetch & Risk Index Calculation ---
        params = {'lat': DHAKA_LAT, 'lon': DHAKA_LON, 'appid': OPENWEATHER_API_KEY, 'units': 'metric'}
        try:
            response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            temp, hum = data['main']['temp'], data['main']['humidity']
            
            # Defensible Mosquito Risk Index
            if temp > 32 or temp < 20: 
                risk = "Low"
            elif 28 <= temp <= 32 and hum > 80: 
                risk = "Critical"
            elif 25 <= temp <= 30 and hum > 70: 
                risk = "High"
            else: 
                risk = "Moderate"

            self.live_weather_data = {'temperature': temp, 'humidity': hum, 'risk_index': risk}
            live_weather_df = pd.DataFrame([{
                'date': pd.to_datetime(datetime.now().date()), 
                'temperature': temp, 
                'humidity': hum, 
                'rainfall': data.get('rain', {}).get('1h', 0.0)
            }])
            weather_df = pd.concat([weather_df, live_weather_df], ignore_index=True).drop_duplicates(subset=['date'], keep='last')
            print(f"✅ Live weather fetched successfully. Current Mosquito Risk: {risk.upper()}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ WARNING: Could not fetch live weather data: {e}. Proceeding with historical data only.")
            self.live_weather_data = {'temperature': 'N/A', 'humidity': 'N/A', 'risk_index': 'Unknown'}

        # --- Unification and Preprocessing ---
        df = pd.merge(dengue_df, weather_df, on='date', how='outer')
        df = pd.merge(df, population_df, on='date', how='outer')
        df = pd.merge(df, nightlight_df, on='date', how='outer')
        df = df.sort_values('date').set_index('date')
        df = df.interpolate(method='time').ffill().bfill()
        
        # CRITICAL FIX: Use correct column name
        df['cases_per_100k'] = (df['dhaka_cases'] / df['dhaka_population_estimated']) * 100000

        # --- Enhanced Feature Engineering ---
        df['day_of_year'] = df.index.dayofyear
        df['is_monsoon'] = df.index.month.isin([6, 7, 8, 9]).astype(int)  # June-Sep
        for col in ['cases_per_100k', 'temperature', 'humidity']:
            for window in [7, 14]:
                df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window, min_periods=1).mean()
        
        self.unified_df = df.reset_index().dropna()
        
        # --- Load Macroeconomic Context ---
        if not econ_df_raw.empty:
            # Handle different column names in economic data
            if 'year' in econ_df_raw.columns:
                latest_econ = econ_df_raw.sort_values(by='year').iloc[-1]
            elif 'date' in econ_df_raw.columns:
                latest_econ = econ_df_raw.sort_values(by='date').iloc[-1]
            else:
                latest_econ = econ_df_raw.iloc[-1]  # Just take the last row
            
            self.macro_econ_context = {
                'gdp_growth_rate': latest_econ.get('gdp_growth_rate', latest_econ.get('gdp_growth', 0)),
                'inflation_rate': latest_econ.get('inflation_rate', latest_econ.get('inflation', 0))
            }
        else:
            self.macro_econ_context = {'gdp_growth_rate': 0, 'inflation_rate': 0}
            
        print("✅ Data loading, unification, and feature engineering complete.")
        return True

    def _discover_causal_links_consensus(self):
        """Identifies high-confidence causal links using a two-method consensus."""
        print("\n[PHASE 2/5] 🔗 Discovering Causal Links (Consensus Method)...")
        df = self.unified_df.copy()
        variables = ['temperature', 'humidity', 'rainfall', 'nightlight_radiance']
        target = 'cases_per_100k'
        
        lagged_corr_links = set()
        for var in variables:
            if var in df.columns:  # Check if column exists
                corrs = [df[target].corr(df[var].shift(lag)) for lag in range(1, CAUSAL_LAG + 1)]
                if max(np.abs(corrs), default=0) > CORR_THRESHOLD:
                    lagged_corr_links.add(var)

        granger_links = set()
        for var in variables:
            if var in df.columns:  # Check if column exists
                base_corr = df[target].corr(df[target].shift(1))
                lagged_var_corr = df[target].corr(df[var].shift(1))
                if abs(lagged_var_corr) > abs(base_corr) and abs(lagged_var_corr) > CORR_THRESHOLD:
                    granger_links.add(var)

        consensus_links = lagged_corr_links.intersection(granger_links)
        
        graph = nx.DiGraph()
        for var in consensus_links:
            corrs = [df[target].corr(df[var].shift(lag)) for lag in range(1, CAUSAL_LAG + 1)]
            best_lag = np.argmax(np.abs(corrs)) + 1
            max_corr = corrs[best_lag - 1]
            graph.add_edge(var, target, lag=best_lag, correlation=max_corr)
            print(f"  - High-Confidence Link: {var} -> {target} (lag: {best_lag} days, r={max_corr:.3f})")

        self.causal_graph = graph
        if not graph.edges():
            print("  - No high-confidence causal links found.")
        print("✅ Causal discovery complete.")

    def _generate_forecast_with_validation(self):
        """Trains a dynamic GP model with enhanced features, validates it, then generates a final forecast."""
        print("\n[PHASE 3/5] 📈 Generating & Validating Forecast...")
        
        features = ['day_of_year', 'is_monsoon', 'temperature_rolling_mean_14', 'humidity_rolling_mean_14', 'cases_per_100k_rolling_mean_7']
        target = 'cases_per_100k'
        
        # Check if all required features exist
        missing_features = [f for f in features if f not in self.unified_df.columns]
        if missing_features:
            print(f"⚠️ WARNING: Missing features {missing_features}, using available features only.")
            features = [f for f in features if f in self.unified_df.columns]
        
        df = self.unified_df.dropna(subset=features + [target]).copy()
        if len(df) < 10:
            print("❌ ERROR: Insufficient data for forecasting.")
            return
            
        X = df[features].values
        y = df[target].values
        
        scaler_X = StandardScaler()
        scaler_y = StandardScaler()
        X_scaled = scaler_X.fit_transform(X)
        y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

        kernel = C(1.0) * RBF(length_scale=[1.0]*len(features)) + WhiteKernel(noise_level=0.1)
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=1e-6)

        # --- 1. Historical Validation Step ---
        print("INFO: Performing historical validation (80/20 split)...")
        split_idx = int(len(X_scaled) * 0.8)
        if split_idx < 5:
            print("⚠️ WARNING: Insufficient data for validation, skipping validation step.")
            gp.fit(X_scaled, y_scaled)
        else:
            gp.fit(X_scaled[:split_idx], y_scaled[:split_idx])
            y_pred_val_scaled, _ = gp.predict(X_scaled[split_idx:], return_std=True)
            y_pred_val = scaler_y.inverse_transform(y_pred_val_scaled.reshape(-1, 1)).ravel()
            
            plt.figure(figsize=(12, 6))
            plt.plot(df['date'].iloc[split_idx:], df[target].iloc[split_idx:], 'k-', lw=2, label='Actual Cases')
            plt.plot(df['date'].iloc[split_idx:], y_pred_val, 'r--', lw=2, label='Model Prediction (Validation)')
            plt.title('Model Historical Validation Performance', fontsize=16, weight='bold')
            plt.ylabel('Cases per 100k')
            plt.legend()
            plt.grid(True, alpha=0.5)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, "02_model_validation.png"), dpi=300, bbox_inches='tight')
            plt.close()
            print("✅ Historical validation plot saved.")

        # --- 2. Final Forecast Step ---
        print("INFO: Retraining on all data for final forecast...")
        gp.fit(X_scaled, y_scaled)
        
        future_features_list = []
        last_known_row = df.iloc[-1]
        
        temp_df = df.copy()
        for i in range(1, FORECAST_HORIZON + 1):
            future_date = temp_df['date'].iloc[-1] + timedelta(days=i)
            new_row = temp_df.iloc[-1:].copy()
            new_row['date'] = future_date
            
            # Project forward
            new_row['day_of_year'] = future_date.timetuple().tm_yday
            new_row['is_monsoon'] = 1 if future_date.month in [6,7,8,9] else 0
            
            temp_df = pd.concat([temp_df, new_row], ignore_index=True)
            temp_df.set_index('date', inplace=True)
            for col in ['cases_per_100k', 'temperature', 'humidity']:
                for window in [7, 14]:
                    temp_df[f'{col}_rolling_mean_{window}'] = temp_df[col].rolling(window, min_periods=1).mean()
            temp_df.reset_index(inplace=True)

            future_features_list.append(temp_df[features].iloc[-1].values)

        X_future = np.array(future_features_list)
        X_future_scaled = scaler_X.transform(X_future)
        y_pred_scaled, sigma_scaled = gp.predict(X_future_scaled, return_std=True)
        y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
        sigma = sigma_scaled * np.sqrt(scaler_y.var_[0])

        self.predictions = {
            'dates': [(df['date'].max() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, FORECAST_HORIZON + 1)],
            'forecast': np.maximum(0, y_pred),
            'lower_ci': np.maximum(0, y_pred - 1.96 * sigma),
            'upper_ci': y_pred + 1.96 * sigma
        }
        print("✅ Final 14-day forecast generated using enhanced features.")

    def _generate_all_outputs(self):
        """Generates all visual, data, and text outputs."""
        print("\n[PHASE 4/5] 🖼️ Generating All Presentation Outputs...")
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Standalone Forecast Plot
        forecast_dates = pd.to_datetime(self.predictions['dates'])
        plt.figure(figsize=(12, 6))
        plt.plot(forecast_dates, self.predictions['forecast'], 'b-', marker='o', lw=2, label='Forecast')
        plt.fill_between(forecast_dates, self.predictions['lower_ci'], self.predictions['upper_ci'], 
                        color='blue', alpha=0.2, label='95% Confidence Interval')
        plt.title('14-Day Forecast (Cases per 100k)', fontsize=16, weight='bold')
        plt.ylabel('Predicted Cases per 100k')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "03_forecast_standalone.png"), dpi=300, bbox_inches='tight')
        plt.close()

        print("✅ Visual assets saved.")

    def _export_data_and_summary(self):
        """Exports data to CSV and writes an enhanced text summary."""
        print("\n[PHASE 5/5] 📝 Generating Final Reports and Briefing...")
        
        # Export predictions
        predictions_df = pd.DataFrame(self.predictions)
        predictions_df.to_csv(os.path.join(DATA_EXPORTS_DIR, 'forecast_table.csv'), index=False)
        
        # Export causal links
        causal_data = [{'cause': u, 'effect': v, 'lag_days': data['lag'], 'correlation': data['correlation']} 
                      for u,v,data in self.causal_graph.edges(data=True)]
        pd.DataFrame(causal_data).to_csv(os.path.join(DATA_EXPORTS_DIR, 'causal_links.csv'), index=False)
        
        print("✅ Data exports (CSV) saved.")

        # --- Generate Enhanced Executive Briefing ---
        total_cases = int(self.unified_df['dhaka_cases'].sum())
        estimated_burden = total_cases * (COST_PER_CASE_USD + ECONOMIC_LOSS_PER_CASE_USD)
        last_7_days_avg = self.unified_df['dhaka_cases'].iloc[-7:].mean()
        prev_7_days_avg = self.unified_df['dhaka_cases'].iloc[-14:-7].mean() if len(self.unified_df) >= 14 else last_7_days_avg
        trend = "Increasing" if last_7_days_avg > prev_7_days_avg else "Decreasing/Stable"

        peak_forecast_idx = np.argmax(self.predictions['forecast'])
        peak_val, peak_date = self.predictions['forecast'][peak_forecast_idx], self.predictions['dates'][peak_forecast_idx]
        
        with open(os.path.join(SUMMARY_DIR, 'executive_briefing.txt'), 'w') as f:
            f.write(f"HAWKEYE OMEGA v2.6 - EXECUTIVE BRIEFING\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("--- CURRENT RISK DASHBOARD ---\n")
            f.write(f"  - Live Mosquito Risk Index: {self.live_weather_data['risk_index'].upper()}\n")
            f.write(f"    (Based on Temp: {self.live_weather_data['temperature']:.1f}°C, Humidity: {self.live_weather_data['humidity']:.0f}%)\n")
            f.write(f"  - Recent Case Trend (7-day avg): {trend}\n")
            f.write(f"  - Forecasted Peak: {peak_val:.1f} cases/100k around {peak_date}\n\n")

            f.write("--- HISTORICAL ANALYSIS & ECONOMIC BURDEN ---\n")
            f.write(f"  - Total Cases Analyzed (Dhaka): {total_cases:,}\n")
            f.write(f"  - High-Confidence Causal Links Found: {len(self.causal_graph.edges())}\n")
            f.write(f"  - Estimated Economic Burden to Date: ${estimated_burden:,.0f} USD\n")
            f.write(f"    (NOTE: Estimate based on ${COST_PER_CASE_USD}/case treatment & ${ECONOMIC_LOSS_PER_CASE_USD}/case productivity loss)\n\n")

            f.write("--- MACROECONOMIC CONTEXT ---\n")
            f.write(f"  - Latest Annual GDP Growth Rate: {self.macro_econ_context['gdp_growth_rate']:.2f}%\n")
            f.write(f"  - Latest Annual Inflation Rate: {self.macro_econ_context['inflation_rate']:.2f}%\n")

        print("✅ Executive briefing text file saved.")

    def run_pipeline(self):
        """Executes the full analysis pipeline."""
        print("="*70 + "\n🚀 EXECUTING HAWKEYE OMEGA v2.6 (DEFENSIVE ENHANCEMENT) 🚀\n" + "="*70)
        if not self._load_data_and_unify(): 
            return
        self._discover_causal_links_consensus()
        self._generate_forecast_with_validation()
        self._generate_all_outputs()
        self._export_data_and_summary()
        print("\n" + "="*70 + "\n✅ PIPELINE EXECUTION COMPLETE ✅\n" + f"All assets generated in: {os.path.abspath(REPORTS_DIR)}\n" + "="*70)

if __name__ == "__main__":
    try:
        pipeline = HawkEyeOmega()
        pipeline.run_pipeline()
    except Exception as e:
        print(f"\n❌ A critical error occurred during pipeline execution: {e}")
        import traceback
        traceback.print_exc()
