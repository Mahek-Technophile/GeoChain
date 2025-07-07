import geopandas as gpd

# Try to load multipolygon features (admin boundaries) from .osm.pbf
path = "data/boundary/Bombay.osm.pbf"

try:
    gdf = gpd.read_file(path, layer='multipolygons')
    print("✅ .osm.pbf loaded successfully")

    # Filter for Mumbai
    mumbai = gdf[gdf['name'].str.contains('Mumbai', case=False, na=False)]

    if not mumbai.empty:
        mumbai.to_file("data/boundary/mumbai_boundary.geojson", driver='GeoJSON')
        print("✅ Mumbai boundary saved to mumbai_boundary.geojson")
    else:
        print("❌ No 'Mumbai' found in the data.")
except Exception as e:
    print("❌ Could not read .osm.pbf directly.")
    print("Error:", e)
