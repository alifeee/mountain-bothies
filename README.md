# Mountain Bothies

Scraping of Mountain Bothie locations from the Mountain Bothie website <https://www.mountainbothies.org.uk/bothies/location-map/>.

Info output as `geoJSON` file -> [`bothies.geojson`](./bothies.geojson), for example,

```json
...
{
    "type": "Feature",
    "properties": {
        "url": "https://www.mountainbothies.org.uk/bothies/northern-highlands/croft-house-lochstrathy/",
        "features": [
            "Open fire",
            "Strictly no vehicle access",
            "Dogs under strict control"
        ],
        "name": "Croft House (Lochstrathy)",
        "location": "Northern Highlands"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            -4.066687736144918,
            58.412679049987325
        ]
    }
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
