# generate_gee_visuals.py
import ee
import geemap
import os

# --- Configuration ---
GCP_PROJECT_ID = "hyperion-472805"
OUTPUT_DIR = "./reports/figures/"

# --- Initialization ---
try:
    ee.Initialize(project=GCP_PROJECT_ID)
    print("✅ Google Earth Engine Initialized.")
except Exception as e:
    print(f"❌ GEE Initialization Failed: {e}")
    exit()

# Create geometry after initialization
DHAKA_AOI = ee.Geometry.Rectangle([90.25, 23.65, 90.55, 23.95]) # Area of Interest for Dhaka

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 1. Dengue Proxy: Surface Water (NDWI) ---
print("Generating NDWI (Surface Water) map for peak monsoon 2024...")
landsat_image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                  .filterBounds(DHAKA_AOI) \
                  .filterDate('2024-07-01', '2024-09-30') \
                  .sort('CLOUD_COVER') \
                  .first()

ndwi = landsat_image.normalizedDifference(['SR_B3', 'SR_B5']) # Green - NIR
ndwi_params = {'min': 0, 'max': 1, 'palette': ['white', 'lightblue', 'blue', 'darkblue']}

geemap.get_image_thumbnail(
    ndwi,
    os.path.join(OUTPUT_DIR, "gee_surface_water_2024.png"),
    vis_params=ndwi_params,
    dimensions=1000,
    region=DHAKA_AOI
)
print("✅ Saved gee_surface_water_2024.png")


# --- 2. Dengue Proxy: Vegetation Cover (NDVI) ---
print("Generating NDVI (Vegetation Cover) map for peak monsoon 2024...")
ndvi = landsat_image.normalizedDifference(['SR_B5', 'SR_B4']) # NIR - Red
ndvi_params = {'min': 0, 'max': 0.8, 'palette': ['white', 'lightgreen', 'green', 'darkgreen']}

geemap.get_image_thumbnail(
    ndvi,
    os.path.join(OUTPUT_DIR, "gee_vegetation_cover_2024.png"),
    vis_params=ndvi_params,
    dimensions=1000,
    region=DHAKA_AOI
)
print("✅ Saved gee_vegetation_cover_2024.png")


# --- 3. Nightlights: Economic Growth Comparison ---
print("Generating Nightlights comparison (2022 vs 2025)...")
viirs_collection = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG").select('avg_rad')

# 2022 Image
image_2022 = viirs_collection.filterDate('2022-01-01', '2022-12-31').median()
# 2025 Image
image_2025 = viirs_collection.filterDate('2025-01-01', '2025-08-31').median()

nl_params = {'min': 0, 'max': 60, 'palette': ['black', 'yellow', 'orange', 'white']}

# Save 2022 image
geemap.get_image_thumbnail(
    image_2022,
    os.path.join(OUTPUT_DIR, "gee_nightlights_2022.png"),
    vis_params=nl_params,
    dimensions=1000,
    region=DHAKA_AOI
)
print("✅ Saved gee_nightlights_2022.png")

# Save 2025 image
geemap.get_image_thumbnail(
    image_2025,
    os.path.join(OUTPUT_DIR, "gee_nightlights_2025.png"),
    vis_params=nl_params,
    dimensions=1000,
    region=DHAKA_AOI
)
print("✅ Saved gee_nightlights_2025.png")

print("\nAll GEE visuals generated successfully in reports/figures/.")