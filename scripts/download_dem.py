import requests

# URL of the SRTM 30m tile covering Mumbai (19N 72E)
url = "https://drop.opentopography.org/raster?opentopoID=OTSRTM.2020.003&west=72.7&south=18.8&east=73.1&north=19.4&outputFormat=GTiff"

# Output path
output_path = "data/elevation/dem_raw.tif"

# Download
print("⬇️ Downloading DEM...")
response = requests.get(url, stream=True)

if response.status_code == 200:
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ Download complete: {output_path}")
else:
    print(f"❌ Failed to download DEM. Status code: {response.status_code}")
