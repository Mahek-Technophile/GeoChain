import rasterio
import geopandas as gpd
from rasterio.mask import mask

# Paths
input_raster = "data/elevation/N19E072.hgt"
boundary_path = "data/boundary/Mumbai.geojson"
output_clipped = "data/elevation/dem_mumbai_clipped.tif"

# Open Mumbai boundary
print("📍 Loading Mumbai boundary...")
boundary = gpd.read_file(boundary_path).to_crs('EPSG:4326')
shapes = [feature["geometry"] for feature in boundary.__geo_interface__["features"]]

# Open and clip the raster
print("🗺️  Clipping DEM...")
with rasterio.open(input_raster) as src:
    out_image, out_transform = mask(src, shapes, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",  # force GeoTIFF
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    with rasterio.open(output_clipped, "w", **out_meta) as dest:
        dest.write(out_image)

print("✅ Done! Saved to:", output_clipped)
