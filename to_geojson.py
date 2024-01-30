"""converts bothies.json to geojson format"""

import json
from OSGridConverter import grid2latlong

BOTHIE_CACHE_FILE = "bothies.json"


def load_cache():
    """loads cache from file"""
    with open(BOTHIE_CACHE_FILE, "r", encoding="utf-8") as cache_file:
        return json.load(cache_file)


def main():
    """main"""
    bothies = load_cache()
    geojson = {"type": "FeatureCollection", "features": []}
    for url, info in bothies.items():
        grid_ref = info["grid_ref"]
        if grid_ref:
            coords = grid2latlong(grid_ref)
            lat, lon = coords.latitude, coords.longitude
            # print(f"{url} {grid_ref} {lat} {lon}")

            geojson["features"].append(
                {
                    "type": "Feature",
                    "properties": {
                        "url": url,
                        "features": info["features"],
                        "name": info["name"],
                    },
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                }
            )
    with open("bothies.geojson", "w", encoding="utf-8") as geojson_file:
        json.dump(geojson, geojson_file)


if __name__ == "__main__":
    main()
