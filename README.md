# Mountain Bothies

Scraping of Mountain Bothie locations from the Mountain Bothie website <https://www.mountainbothies.org.uk/bothies/location-map/>.

Info output as `geoJSON` file -> [`bothies.geojson`](./bothies.geojson), for example,

```json
...
    "https://www.mountainbothies.org.uk/bothies/southwest-highlands-islands/essan/": {
        "grid_ref": "NM 817 817",
        "features": [
            "Sleeping Bunks",
            "Open fire",
            "Fuel scarce"
        ]
    },
...
```

Load this file on any mapping software, such as <https://geojson.io/>.

## Development

Requirements: Python 3

### Install dependencies

```bash
pip install -r requirements.txt
```

### Get bothies

```bash
py get_bothies.py
```

### Convert data to `geoJSON`

```bash
py to_geojson.py
```
